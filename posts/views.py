from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.views import generic

from braces.views import SelectRelatedMixin

from . import models
from . import forms

from user_profile.models import UserProfile

# Create your views here.
user_model = get_user_model()

class PostList(LoginRequiredMixin, SelectRelatedMixin, generic.ListView):
    model = models.Post
    select_related = ('user', )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_posts'] = UserProfile.objects.get(user__exact=self.request.user).likes.all()
        return context


class UserPosts(LoginRequiredMixin, generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
    
    def get_queryset(self):
        try:
            self.post_user = user_model.objects.prefetch_related('posts').get(
                username__iexact=self.kwargs.get('slug'))
        except user_model.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        context['liked_posts'] = UserProfile.objects.get(user__exact=self.request.user).likes.all()
        return context
    

class PostDetail(LoginRequiredMixin, SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ('user', )

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get('slug'))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['liked_posts'] = UserProfile.objects.get(user__exact=self.request.user).likes.all()
        return context


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


class LikeView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.POST.get('next', reverse('posts:all'))

    def get(self, request, *args, **kwargs):
        try:
            liking_user_profile = UserProfile.objects.get(user__exact=self.request.user)
            liked_post = models.Post.objects.get(pk__iexact=self.kwargs.get('pk'))

        except UserProfile.DoesNotExist:
            messages.warning(
                self.request,
                "Something went wrong..."
            )

        else:
            liked_post.like(liking_user_profile)
            messages.success(
                self.request,
                "You liked a post."
            )
        return super().get(request, *args, **kwargs)


class UnlikeView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.POST.get('next', reverse('posts:all'))

    def get(self, request, *args, **kwargs):
        try:
            liking_user_profile = UserProfile.objects.get(user__exact=self.request.user)
            liked_post = models.Post.objects.get(pk__iexact=self.kwargs.get('pk'))

        except UserProfile.DoesNotExist:
            messages.warning(
                self.request,
                "Something went wrong..."
            )

        else:
            liked_post.unlike(liking_user_profile)
            messages.success(
                self.request,
                "You unliked a post."
            )
        return super().get(request, *args, **kwargs)
    
class UserLikesPostsList(LoginRequiredMixin, generic.ListView):
    model = models.Post
    template_name = 'posts/user_likes_post_list.html'
    
    def get_queryset(self):
        try:
            self.user_likes_post = UserProfile.objects.get(
                slug__iexact=self.kwargs.get('slug'))
        except user_model.DoesNotExist:
            raise Http404
        else:
            return self.user_likes_post.likes.all()
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_likes_post'] = self.user_likes_post
        context['liked_posts'] = UserProfile.objects.get(user__exact=self.request.user).likes.all()
        return context