from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
import json


class ProfileCfn(models.Model):
    """The profile model for a CFN user."""

    user = models.OneToOneField(
        User,
        related_name='profile',
        on_delete=models.CASCADE,
    )
    about = models.TextField(max_length=1028, blank=True, null=True)
    follows = models.ManyToManyField(User, related_name='followed_by')
    avatar_url = models.URLField(max_length=256, null=True, blank=True)

    @property
    def is_active(self):
        """Return true if the user is authenticated."""
        return self.user.is_active

    def __str__(self):
        """String representation of profile."""
        return self.user.username


@receiver(post_save, sender=User)
def make_user_profile(sender, instance, **kwargs):
    """Create and save a profile when a user is created."""
    if kwargs["created"]:
        profile = ProfileCfn(user=instance)
        try:
            # req = github_api_call(str(profile)) #<-- maybe use
            # req = requests.get('https://api.github.com/users/' + str(profile))

            # content = req.content.decode('utf-8')
            # json_list.append(json.loads(content))
            content = github_api_call(str(profile))
            json_list = []
            json_list.append(json.loads(content))
            if json_list[0]['avatar_url']:
                profile.avatar_url = json_list[0]['avatar_url']
            profile.about = json_list[0]['bio']
        except:
            pass
        profile.save()


def github_api_call(profile_str):
    """Make api call to github to retrieve user data."""
    print('api cal here!!!!!!!')
    req = requests.get('https://api.github.com/users/' + profile_str)
    content = req.content.decode('utf-8')
    return content

