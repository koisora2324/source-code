from django.shortcuts import render
from django.http import HttpResponse
from users.models import User
from django.http import JsonResponse
from django.shortcuts import redirect


# Create your views here.
# /register/
def register(request):
    """注册View视图函数"""
    # 注册页面内容
    # html = """
    # <html>
    #     <head>
    #         <title>注册页面</title>
    #     </head>
    #     <body>
    #         <form method='post' action='/register'>
    #             username:<input type='text' name='username'/><br/>
    #             password:<input type='password' name='password'/><br/>
    #             <input type='submit' value='注册' />
    #         </form>
    #     </body>
    # </html>
    # """
    # # 返回响应
    # return HttpResponse(html)

    # return render(request, 'register.html')
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        # 获取表单post提交的用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username:%s password:%s' % (username, password))
        #
        # return HttpResponse('进行注册业务处理')
        # 注册用户信息数据的保存
        # create方法的返回的是一个User模型对象,对应的是用户表中的注册用户的数据
        user = User.objects.create(username=username, password=password)
        #
        # return HttpResponse('注册成功')
        # return JsonResponse({'message': '注册成功'})
        return redirect('/login/')


def login(request):
    """登录view视图函数"""
    # 使用模板文件login.html,返回登录函数
    # return render(request, 'login.html')
    username = request.session.get('username')
    if username:
        # username 在session中存在,则用户已登录
        return HttpResponse('%s用户已登录' % username)

    if request.method == 'GET':
        # 返回登录界面
        # return render(request, 'login.html')
        # username = request.COOKIES.get('username')
        #
        # # 返回登录页面
        # return render(request, 'login.html', context={'username': username})
        return render(request, 'login.html')
    else:
        # 登录业务逻辑
        # 获取username 和 password
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        # 进行用户名和密码校验
        try:
            # 根据 username 和 password 查询对应的用户是否存在,即进行用户名和密码校验
            # get 方法默认会利用查询到的数据创建一个对应的模型类对象,并将这个模型对象返回
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            # 如果get方法查询不到数据,会出现'模型类.DoesNotExist'异常
            # 用户名或密码错误
            return JsonResponse({'message': 'login failed'})
        else:
            # 用户名和密码正确
            # 1.return JsonResponse({'message': 'login success'})
            # 2.response = JsonResponse({'message': 'login success'})
            # # 判断是否需要记住登录用户名
            # if remember == 'true':
            #     # 记住登录用户名,设置cookie数据,有效期为14天
            #     response.set_cookie('username', username, max_age=14 * 24 * 3600)
            #
            # return response
            request.session['user_id'] = user.id
            request.session['username'] = user.username

            if remember != 'true':
                # 不记住登录,将session的标识cookie设置为浏览器关闭即失效
                request.session.set_expiry(0)

            return JsonResponse({'message': 'login success'})
