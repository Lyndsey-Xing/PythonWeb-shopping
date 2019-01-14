from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template.context_processors import request
from datetime import datetime
from django.template.loader import get_template
from django.http.response import HttpResponseRedirect
import os
from keystoneclient.v3 import client as lient
from swiftclient import client
from django.http import StreamingHttpResponse
from swiftclient import ClientException
# Create your views here.
#keystone认证和swiftclient连接
def connect():
     #con = lient.Client(
        #user_domain_name=os.environ['OS_USER_DOMAIN_NAME'],
        #username=os.environ['OS_USERNAME'],
        #password=os.environ['OS_PASSWORD'],
        #project_domain_name=os.environ['OS_PROJECT_DOMAIN_NAME'],
        #project_name=os.environ['OS_PROJECT_NAME'],
        #auth_url=os.environ['OS_AUTH_URL']                     
        #    )
		#keystone认证
    _authurl = 'http://object:35357/v3'
    _auth_version = '3'
    _user = 'admin'
    _key = '684739'
    _os_options = {
        'user_domain_name': 'default',
        'project_domain_name': 'default',
        'project_name': 'admin'
    }
#swiftclient连接
    conn = client.Connection(
       authurl=_authurl,
       user=_user,
       key=_key,
       os_options=_os_options,
       auth_version=_auth_version
    )
    return conn
#登录
def login(request):
    if request.method=='POST':
        user=request.POST['username']
        password=request.POST['password']
        if user=='admin' and password=='684739':
            request.session['username']=user
            return HttpResponseRedirect('/myblogs/lists/')
        else:
            message='input user and password'
            return render(request,'myblogs/login.html',locals())
    return render(request,'myblogs/login.html')   
#退出
def logout(request):
    del request.session['username'] 
#     auth.logout(request)
    return  render(request,'myblogs/login.html',locals())               
#上传
def upload(request):
    user=request.session.get('username')
    if user!=None:
        if request.method=='POST':
		    #把客户端的文件上传到虚拟机上
            file =request.FILES.get('file',None)
            if not file:
                message="upload file"
                return render(request,'myblogs/upload.html',locals())
            else:
                with open("/tmp/%s" % file.name,'wb+') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
			#把上传到虚拟机上的文件再上传到swift的容器里面
                conn=connect()
                container = 'Ben'
                with open("/tmp/%s" % file.name, 'r') as local:
                    conn.put_object(
                        container,
                        file.name,
                        contents=local,
                        content_type='text/plain'
                    )
                message="upload sccessful"
                return HttpResponseRedirect('/myblogs/lists/')
        else:
            return render (request,'myblogs/upload.html',locals())
    else:
        return render(request,'myblogs/login.html')
#下载
def download(request):
    user=request.session.get('username')
    if user!=None:
	    #把swift容器里面的对象下载到虚拟机里面
        conn=connect()
        objs = request.GET['object']
        obj=objs.strip('"').strip()
        container = 'Ben'
        resp_headers, obj_contents = conn.get_object(container, obj)
        with open('/home/jia/file/%s' % obj, 'w') as local:
            local.write(obj_contents)
		#再把下载到虚拟机里面的文件下载到客户端
        def file_iterator(file, chunk_size=512):
            with open(file) as f:
                while True:
                    c = f.read(chunk_size)
                    if c:
                        yield c
                    else:
                        break
     
        file = "/home/jia/file/%s" % obj
        response = StreamingHttpResponse(file_iterator(file))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file)
        return response
    else:
        return render(request,'myblogs/login.html')
#列出上传到容器里面的对象
def lists(request):
    user=request.session.get('username')
    if user!=None:
        num=0
        conn=connect()
        resp_headers,objects = conn.get_container('Ben')
        return render(request,'myblogs/lists.html',locals())
    else:
        return render(request,'myblogs/login.html')
#删除容器里面的对象
def delete(request):
    user=request.session.get('username')
    if user!=None:
        conn=connect()
        objs = request.GET['object']
        obj=objs.strip('"').strip()
        container = 'Ben'
        try:
            conn.delete_object(container, obj)
            message="Successfully deleted the object"
        except ClientException as e:
            message="Failed to delete the object with error: %s" % e
        return HttpResponseRedirect('/myblogs/lists/')
    else:
        return render(request,'myblogs/login.html')

