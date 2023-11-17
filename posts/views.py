from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models
from . import forms

# Create your views here.
User = get_user_model()

class PostList(LoginRequiredMixin, SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', )


class UserPosts(LoginRequiredMixin, generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
    
    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('slug'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context
    

class PostDetail(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get('slug'))


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # fields = ('message', 'picture')
    model = models.Post
    form_class = forms.PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        # # Check if they provided a profile picture
        # if 'profile_pic' in request.FILES:
        #     print('found it')
        #     # If yes, then grab it from the POST form reply
        #     profile.profile_pic = request.FILES['profile_pic']
        self.object.save()
        return super().form_valid(form)
    

class DeletePost(LoginRequiredMixin, SelectRelatedMixin,generic.DeleteView):
    model = models.Post
    select_related = ('user', )
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id = self.request.user.id)
    
    def delete(self, *args, **kwargs):
        messages.success(self.request, 'Post Deleted')
        return super().delete(*args, **kwargs)
    