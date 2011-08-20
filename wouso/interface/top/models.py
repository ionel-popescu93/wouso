from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth.models import User
from wouso.core.app import App
from wouso.core.user.models import UserProfile
from wouso.interface import render_string


class TopUser(UserProfile):

    @property
    def progress(self):
        try:
            yesterday = History.objects.filter(user=self).order_by('-date')[0]
            daybefore = History.objects.filter(user=self).order_by('-date')[1]
        except Exception as e:
            return 0
        return yesterday.position - daybefore.position

    @property
    def weeklyprogress(self):
        try:
            yesterday     = History.objects.filter(user=self).order_by('-date')[0]
            day1weekprior = History.objects.filter(user=self).order_by('-date')[7]
        except Exception as e:
            return 0
        return yesterday.position - day1weekprior.position

class History(models.Model):
    user = models.ForeignKey('TopUser');
    position = models.IntegerField();
    points = models.IntegerField();
    date = models.DateField();

class Top(App):

    @classmethod
    def get_sidebar_widget(kls, request):
        top5 =TopUser.objects.all().order_by('-points')[:5]
        return render_string('top/sidebar.html',
            {'topusers': top5}
        )

def user_post_save(sender, instance, **kwargs):
    profile = instance.get_profile()
    profile.get_extension(TopUser)
models.signals.post_save.connect(user_post_save, User)

