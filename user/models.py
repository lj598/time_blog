from django.db import models
from django.contrib.auth.models import User
# 基于系统自带User进行拓展models

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.DO_NOTHING,verbose_name="昵称")#设定一个和User一对一的外键关联
    nickname = models.CharField(max_length=32)
    def __str__(self):
        return '<Profile: %s for %s>' % (self.nickname,self.user.username)

def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return self.username
User.get_nickname = get_nickname
