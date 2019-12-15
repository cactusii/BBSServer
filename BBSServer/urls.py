from django.urls import path,include
from .views import *


urlpatterns = [
    path('test',test),
    path('login',login),
    path('register',register),
    path('forgetpassword',forgetPassword),
    path('forgetpassword2',forgetPassword2),
    path('getuserinfo',getUserInfo),
    path('yanzheng',yanzheng),
    path('uploadUserInfo',uploadUserInfo),
    path('uploadImage', uploadImage),
    path('posttiezi',postTiezi),
    path('writePic',writePic),
    path('downloadAllTiezi',downloadAllTiezi),
    path('downloadImage',downloadImage),
    path('downloadComment',downloadComment),
    path('getGuanzhu',getGuanzhu),
    path('guanzhu',guanzhu),
    path('dianzan',dianzan),
    path('getDianzan',getDianzan),
    path('comment',comment),
    path('commentDianzan',commentDianzan),
    path('getCommentDianzan',getCommentDianzan)
]
