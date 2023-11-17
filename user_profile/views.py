from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import UserProfileUpdateForm
from . import models
from accounts.forms import UserUpdateForm

user_model = get_user_model()

class UserProfileUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = models.UserProfile
    form_class = UserProfileUpdateForm
    second_form_class = UserUpdateForm
    template_name = 'user_profile/edit_profile.html'

    def get_object(self):
        active_user_profile = models.UserProfile.objects.get(user=self.request.user)
        return active_user_profile

    def get_context_data(self, **kwargs):
        context = super(UserProfileUpdateView, self).get_context_data(**kwargs)
        if 'user_form' not in context:
            context['user_form'] = self.second_form_class(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.form_class(request.POST,
                               request.FILES,
                               instance=request.user.userprofile)
        user_form = self.second_form_class(request.POST, instance=request.user)

        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(self.request, 'Profile updated successfully')
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.render_to_response(
              self.get_context_data(form=form, user_form=user_form))

    def get_success_url(self):
        slug = self.get_object().slug
        return reverse_lazy('user_profile:profile_detail', kwargs={'slug': slug})


class ProfileListAll(LoginRequiredMixin, generic.ListView):
    template_name = 'user_profile/profile_list_all.html'
    model = models.UserProfile


class ProfileListFollowing(LoginRequiredMixin, generic.ListView):
    template_name = 'user_profile/profile_list_following.html'
    model = models.UserProfile

    def get_queryset(self, *args, **kwargs): 
        following = models.UserProfile.objects.get(slug__iexact=self.kwargs.get('slug')).following.all()
        queryset = super(ProfileListFollowing, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(user__in=following)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_details'] = models.UserProfile.objects.get(slug__iexact=self.kwargs.get('slug'))
        return context


class ProfileListFollowers(LoginRequiredMixin, generic.ListView):
    template_name = 'user_profile/profile_list_followers.html'
    model = models.UserProfile

    def get_queryset(self, *args, **kwargs): 
        followers = models.UserProfile.objects.get(slug__iexact=self.kwargs.get('slug')).followers.all()
        queryset = super(ProfileListFollowers, self).get_queryset(*args, **kwargs)
        queryset = queryset.filter(user__in=followers)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_details'] = models.UserProfile.objects.get(slug__iexact=self.kwargs.get('slug'))
        return context


class ProfileDetail(LoginRequiredMixin, generic.DetailView):
    model = models.UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_details'] = user_model.objects.get(username__iexact=self.kwargs.get('slug'))
        profile_details = models.UserProfile.objects.get(slug__iexact=self.kwargs.get('slug'))
        is_following = self.request.user in profile_details.followers.all()
        context['is_following'] = is_following
        return context


class FollowView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("user_profile:profile_detail", kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            following_user_profile = models.UserProfile.objects.filter(
                user=self.request.user,
            ).get()
            followed_user_profile = models.UserProfile.objects.filter(
                slug=self.kwargs.get("slug")
            ).get()

        except models.UserProfile.DoesNotExist:
            messages.warning(
                self.request,
                "Something went wrong..."
            )

        else:
            following_user_profile.follow(followed_user_profile)
            messages.success(
                self.request,
                "You started to follow " + followed_user_profile.slug + "."
            )
        return super().get(request, *args, **kwargs)


class UnfollowView(LoginRequiredMixin, generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse("user_profile:profile_detail", kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            following_user_profile = models.UserProfile.objects.filter(
                user=self.request.user,
            ).get()
            followed_user_profile = models.UserProfile.objects.filter(
                slug=self.kwargs.get("slug")
            ).get()

        except models.UserProfile.DoesNotExist:
            messages.warning(
                self.request,
                "Something went wrong..."
            )

        else:
            following_user_profile.unfollow(followed_user_profile)
            messages.success(
                self.request,
                "You stopped following " + followed_user_profile.slug + "."
            )
        return super().get(request, *args, **kwargs)