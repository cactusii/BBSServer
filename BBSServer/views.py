import datetime
import traceback
import smtplib
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# from django.shortcuts import render
from django.http import HttpResponse
import BBSServer.models as bm
import json
from BBSServer import utils

# 执行响应的逻辑代码，最主要的代码编辑区
# Create your views here.
from HBUBBSServer import settings

'''
增 bm.Id.objects.create
删 bm.Id.objects.filter(sch_id=sch_id).delete()
改 user = bm.Id.objects.get(sch_id=sch_id) user.password=newpassword
查 bm.Id.objects.all() 
只取title列 字典类型
objects.all().values('title') 
只有value值 tuple类型
objects.all().values_list('title') 
模糊查询并去重
objects.filter(title__icontains='python').distinct()
'''


def test(request):
    user = bm.Id.objects.get(sch_id='20161101080')
    print(user.sch_id)
    return HttpResponse('成功！')

def login(request):
    # alluser = list(bm.User.objects.all().values())
    # return JsonResponse(alluser,safe=False)
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
        password = jsonUser['password']
        print(sch_id+" "+password)
    except Exception as e:
        return JsonResponse({'status':'9'})# json数据解析错误

    try:
        user = bm.Id.objects.get(sch_id = sch_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status':'0'})# 用户不存在
    else:
        if(user.status=='0'):
            return JsonResponse({'status':'10'})# 未完成邮箱验证
        elif(password==user.password):
            return JsonResponse({'status':'4'})# 验证正确
        else:
            return JsonResponse({'status':'1'})# 密码错误


def register(request):
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
        password = jsonUser['password']
        email = jsonUser["email"]
        print(sch_id + " " + password + " " +email)
    except:
        return JsonResponse({'status':'9'})

    try:
        user = bm.Id.objects.get(sch_id=sch_id)
    except ObjectDoesNotExist:
        bm.Id.objects.create(sch_id=sch_id, password=password, email=email,status='0')
        user = bm.Id.objects.get(sch_id=sch_id)
        vc = utils.sendEmail(1, email)
        user.verification_code = vc
        user.save()
        return JsonResponse({'status':'4'})
    else:
        print(traceback.print_exc())
        return JsonResponse({'status':'0'})


def yanzheng(request):
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
        vc = jsonUser['vc']
    except:
        return JsonResponse({'status':'9'})

    try:
        user = bm.Id.objects.get(sch_id=sch_id)
        if(user.verification_code == vc):
            user.status = '1'
            user.verification_code = ""
            user.save()
            return JsonResponse({'status':'4'})
        else:
            return JsonResponse({'status':'0'})# 验证码错误
    except:
        print(traceback.print_exc())

def forgetPassword(request):
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
        email = jsonUser["email"]
        print(sch_id + " " +email)
    except:
        return JsonResponse({'status':'9'})

    try:
        user = bm.Id.objects.get(sch_id=sch_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': '0'})
    else:
        if(user.email!=email):
            return JsonResponse({'status':'3'})#学号邮箱不对应
        # 发送邮件验证码
        vc = utils.sendEmail(2,email)
        user.verification_code = vc
        user.save()
        return JsonResponse({'status':'4'})

def forgetPassword2(request):
    print("----------")
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
        password = jsonUser['password']
        vc = jsonUser['vc']
        print(sch_id+password+vc)
    except:
        print(traceback.print_exc())
        return JsonResponse({'status': '9'})

    try:
        user = bm.Id.objects.get(sch_id=sch_id)
    except ObjectDoesNotExist:
        return JsonResponse({'status': '0'})
    else:
        if (user.verification_code != vc):
            return JsonResponse({'status': '3'})  # 验证码错误
        # 修改密码
        user.password=password
        user.verification_code = ""
        user.save()
        return JsonResponse({'status': '4'})


def getUserInfo(request):
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
    except:
        return JsonResponse({"status":'9'})
    try:
        user = bm.User.objects.get(sch_id=sch_id)
        userId = bm.Id.objects.get(sch_id=sch_id)
        userData = {'sch_id': user.sch_id,
                    'email':userId.email,
                    'password':userId.password,
                    'status':'4',
                    'username': user.username,
                    'sex': user.sex,
                    'grade': user.grade,
                    'academy': user.academy,
                    'fatie_num': user.fatie_num,
                    'guanzhu_num': user.guanzhu_num,
                    'shoucang_num': user.shoucang_num,
                    'fensi_num': user.fensi_num,
                    'register_date': user.register_date,
                    'photo':user.photo,
                    'jianjie':user.jianjie}

        # print(userData)
        return JsonResponse(userData)
    except:
        print(traceback.print_exc())
        return JsonResponse({"status":"0"})

def uploadUserInfo(request):
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonUser['sch_id']
    except:
        return JsonResponse({"status":'9'})
    try:
        user = bm.User.objects.get(sch_id=sch_id)
        userId = bm.Id.objects.get(sch_id=sch_id)
        userId.password = jsonUser['password']
        user.username = jsonUser['username']
        user.photo = jsonUser['photo']
        user.fensi_num = jsonUser['fensi_num']
        user.shoucang_num = jsonUser['shoucang_num']
        user.guanzhu_num = jsonUser['guanzhu_num']
        user.fatie_num = jsonUser['fatie_num']
        user.academy = jsonUser['academy']
        user.grade = jsonUser['grade']
        user.sex = jsonUser['sex']
        user.jianjie = jsonUser['jianjie']
        user.save()
        return JsonResponse({"status":"4"})
    except:
        print(traceback.print_exc())
        return JsonResponse({"status":"0"})


def uploadImage(request):
    if(request.method=="POST"):
        img = request.FILES.get("image")
        fname = "%s%s%s"%(settings.MEDIA_ROOT,settings.MEDIA_URL,img.name)
        with open(fname,'wb') as imgsave:
            for i in img.chunks():
                imgsave.write(i)
        return JsonResponse({"status":"4"})


def downloadImage(request):
    try:
        jsonUser = json.loads(request.body.decode("UTF-8"))
        imgName = jsonUser['imgName']
    except:
        return JsonResponse({"status": '9'})

    fpath = "%s%s%s"%(settings.MEDIA_ROOT,settings.MEDIA_URL,imgName)
    with open(fpath, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type="image/png")



def postTiezi(request):
    try:
        jsonTiezi = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonTiezi['sch_id']
        content = jsonTiezi['content']
        tiezi_id = jsonTiezi['tiezi_id']
        print(sch_id+" "+content)
    except:
        return JsonResponse({"status":'9'})
    try:
        bm.Tiezi.objects.create(tiezi_id = tiezi_id,sch_id=sch_id,content=content,dianzan_num=0,liulan_num=0,post_time=datetime.datetime.now())
        user = bm.User.objects.get(sch_id=sch_id)
        user.fatie_num+=1
        user.save()
        return JsonResponse({"status":"4"})
    except:
        print(traceback.print_exc())
        return JsonResponse({"status":"0"})

def downloadAllTiezi(request):
    allTiezi = json.dumps(list(bm.Tiezi.objects.order_by('-post_time').values()),ensure_ascii=False,cls=utils.DateEncoder)
    # print(allTiezi)
    return HttpResponse(allTiezi,content_type="application/json,charset=utf-8")



def writePic(request):
    try:
        jsonPic = json.loads(request.body.decode("UTF-8"))
        pic_id = jsonPic['pic_id']
        tieziId = jsonPic['tieziId']
        index = int(jsonPic['index'])
    except:
        return JsonResponse({'status':'9'})
    bm.Picture.objects.create(pic_id=pic_id,tiezi_id=tieziId,uri=pic_id,index=index)
    return JsonResponse({'status':'4'})


def downloadComment(request):
    try:
        jsonTieziId = json.loads(request.body.decode("UTF-8"))
        tiezi_id = jsonTieziId['tiezi_id']
    except:
        return JsonResponse({'status':'9'})

    try:
        allComment = json.dumps(list(bm.Pinglun.objects.filter(tiezi_id=tiezi_id).order_by('-dianzan_num').values()), ensure_ascii=False,
                             cls=utils.DateEncoder)
    except ObjectDoesNotExist:
        return HttpResponse("0")


    return HttpResponse(allComment, content_type="application/json,charset=utf-8")


def getGuanzhu(request):
    try:
        jsonTieziId = json.loads(request.body.decode("UTF-8"))
        sch_id = jsonTieziId['sch_id']
    except:
        return JsonResponse({'status':'9'})
    try:
        guanzhus = json.dumps(list(bm.Guanzhu.objects.filter(sch_id=sch_id).values()), ensure_ascii=False,
                             cls=utils.DateEncoder)
    except ObjectDoesNotExist:
        return HttpResponse("0")

    return HttpResponse(guanzhus, content_type="application/json,charset=utf-8")


def guanzhu(request):
    try:
        jsonGuanzhu = json.loads(request.body.decode("UTF-8"))
        print(jsonGuanzhu)
        sch_id = jsonGuanzhu['sch_id']
        b_shc_id = jsonGuanzhu['b_sch_id']
    except:
        return JsonResponse({'status':'9'})
    try:
        bm.Guanzhu.objects.create(sch_id=sch_id,b_sch_id=b_shc_id)
        b_user = bm.User.objects.get(sch_id=b_shc_id)
        b_user.fensi_num += 1
        b_user.save()
        user = bm.User.objects.get(sch_id=sch_id)
        user.guanzhu_num += 1
        user.save()
        return HttpResponse("1")
    except:
        bm.Guanzhu.objects.filter(sch_id=sch_id,b_sch_id=b_shc_id).delete()
        b_user = bm.User.objects.get(sch_id=b_shc_id)
        b_user.fensi_num -= 1
        b_user.save()
        user = bm.User.objects.get(sch_id=sch_id)
        user.guanzhu_num -= 1
        user.save()
        return HttpResponse("1")


def dianzan(request):
    try:
        jsonDianzan = json.loads(request.body.decode("UTF-8"))
        print(jsonDianzan)
        sch_id = jsonDianzan['sch_id']
        tp_id = jsonDianzan['tp_id']
    except:
        return JsonResponse({'status': '9'})
    try:
        bm.Dianzan.objects.create(sch_id=sch_id,tp_id=tp_id,type=0)
        tiezi = bm.Tiezi.objects.get(tiezi_id=tp_id)
        tiezi.dianzan_num += 1
        tiezi.save()
        print("点赞")
        return HttpResponse("1")
    except:
        print("删除")
        bm.Dianzan.objects.filter(sch_id=sch_id,tp_id=tp_id).delete()
        tiezi = bm.Tiezi.objects.get(tiezi_id=tp_id)
        tiezi.dianzan_num -= 1
        tiezi.save()
        return HttpResponse("1")

def getDianzan(request):
    try:
        jsonTpId = json.loads(request.body.decode("UTF-8"))
        tp_id = jsonTpId['tp_id']
    except:
        return JsonResponse({'status': '9'})
    try:
        dianzan = json.dumps(list(bm.Dianzan.objects.filter(tp_id=tp_id,type=0).values()), ensure_ascii=False,
                              cls=utils.DateEncoder)
    except ObjectDoesNotExist:
        return HttpResponse("0")

    return HttpResponse(dianzan, content_type="application/json,charset=utf-8")


def comment(request):
    try:
        jsonComment = json.loads(request.body.decode("UTF-8"))
        commentId = jsonComment['id']
        tiezi_id = jsonComment['tiezi_id']
        sch_id = jsonComment['sch_id']
        content = jsonComment['content']
        print(jsonComment)
    except:
        return JsonResponse({"status": '9'})
    try:
        bm.Pinglun.objects.create(id=commentId,tiezi_id=tiezi_id,sch_id=sch_id,time=datetime.datetime.now(),content=content,dianzan_num=0)
        tiezi = bm.Tiezi.objects.get(tiezi_id=tiezi_id)
        tiezi.liulan_num+=1
        tiezi.save()
        return JsonResponse({"status": "4"})
    except:
        print(traceback.print_exc())
        return JsonResponse({"status": "0"})

def commentDianzan(request):
    try:
        jsonDianzan = json.loads(request.body.decode("UTF-8"))
        print(jsonDianzan)
        sch_id = jsonDianzan['sch_id']
        tp_id = jsonDianzan['tp_id']
    except:
        return JsonResponse({'status': '9'})
    try:
        bm.Dianzan.objects.create(sch_id=sch_id,tp_id=tp_id,type=1)
        comm = bm.Pinglun.objects.get(id=tp_id)
        comm.dianzan_num+=1
        comm.save()
        print("点赞")
        return HttpResponse("1")
    except:
        print("删除")
        bm.Dianzan.objects.filter(sch_id=sch_id,tp_id=tp_id,type=1).delete()
        comm = bm.Pinglun.objects.get(id=tp_id)
        comm.dianzan_num -= 1
        comm.save()
        return HttpResponse("1")


def getCommentDianzan(request):
    try:
        jsonTpId = json.loads(request.body.decode("UTF-8"))
        tp_id = jsonTpId['tp_id']
    except:
        return JsonResponse({'status': '9'})
    try:
        dianzan = json.dumps(list(bm.Dianzan.objects.filter(tp_id=tp_id, type=1).values()), ensure_ascii=False,
                             cls=utils.DateEncoder)
    except ObjectDoesNotExist:
        return HttpResponse("0")

    return HttpResponse(dianzan, content_type="application/json,charset=utf-8")
