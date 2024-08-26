from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views import generic
from .models import Group, GroupMember

class CreateGroup(LoginRequiredMixin, generic.edit.CreateView):
    fields = ('name', 'description')
    model = Group
    permission_required = 'groups.add_group'

class SingleGroup(generic.DetailView):
    model = Group

class ListGroups(generic.ListView):
    model = Group

class JoinGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning, You are already a member of this group')
        else:
            messages.success(self.request, 'You are now a member of this group')

        return super().get(request, *args, **kwargs)

class LeaveGroup(LoginRequiredMixin, generic.RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug': self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        try:
            membership = GroupMember.objects.filter(user=self.request.user,
                                                     group__slug=self.kwargs.get('slug')
            ).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'Warning, You are not a member of this group')
        else:
            membership.delete()
            messages.success(self.request, 'You have left the group')

        return super().get(request, *args, **kwargs)
