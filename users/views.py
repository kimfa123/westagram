from django.shortcuts import render

# Create your views here.
import json
from django.views import View
from django.http import JsonResponse, HttpResponse
from .models import Users

# /users/로 들어왔을 때 출력되는 화면
class MainView(View):
  def get(self, request):
    return JsonResponse({'Welcome to':'Westagram', 'Sign-up':'/users/sign-up', 'Log-in':'/users/log-in'}, status=200)

# /users/sign-up/에서 액션에 따라 띄워줄 화면 설정
class SignUpView(View):
  # 데이터를 입력하는 것이므로 get이 아닌 post 메서드를 사용한다.
  def post(self, request):
    data = json.loads(request.body)
        
    # 유저가 입력한 데이터인 data['username']과 data['password']이
    # 각각 username과 password 열에 저장된다.
    try:
      Users(
        username = data['username'],
        password = data['password'],
      ).save()

    # 에러가 발생하면 401코드와 함께 지정한 메시지를 띄운다.
    except:
      return JsonResponse({'message':'INVALID_ID'}, status=401)

    # 에러가 발생하지 않고 잘 작동하면 200코드와 함께 지정한 메시지를 띄운다.
    else:
      return JsonReponse({'message':'WELCOME'}, status=200)
    
  # /users/sign-up/을 호출했을 때 출력되는 화면
  def get(self, request):
    return JsonResponse({'Please':'Sign-up'}, status=200)

# /users/log-in/에서 액션에 따라 띄워줄 화면 설정
class LogInView(View):
  # 데이터를 입력하는 것이므로 get이 아닌 post 메서드를 사용한다.
  def post(self, request):
    data = json.loads(request.body)
    # sign-up과는 달리 데이터를 신규로 입력하는 것이 아니므로 .save()는 쓰지 않는다.
    Users(
      username = data['username'],
      password = data['password']
    )
    
    # 아이디가 유효하면 비밀번호가 유효한지 검사하고,
    # 아이디나 비밀번호가 유효하지 않다면 401코드와 함께 지정한 메시지를 띄운다.
    # 아이디와 비밀번호가 모두 일치한다면 200코드와 함께 지정한 메시지를 띄운다.
    try:
      if Users.objects.filter(username=data['username']).exists():
        user_id = Users.objects.get(username=data['username'])
        if data['password'] == user_id.password:
          return JsonResponse({'message':'WELCOME, ' + data['username']}, status=200)
        else:
          return JsonResponse({'message':'비밀번호가 틀립니다.'}, status=401)
      else:
        return JsonResponse({'message':'아이디가 없습니다.'}, status=401)
    except:
      return JsonResponse({'message':'INVALID_USER'}, status=401)

  # 로그인 정보를 받아서 입력한 유저의 정보만을 호출하고 싶었으나 아래처럼 하면 에러 발생
  def get(self, request):
    login_data = Users.objects.filter(username=data['username']).values()
    return JsonResponse({'user':list(login_data)}, status=200)