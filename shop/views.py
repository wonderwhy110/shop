from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Category, Product
from .forms import  UserRegistrationForm
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm
import requests
from django.contrib import messages
import requests
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .forms import UserRegistrationForm
from django.core.exceptions import ValidationError
from .models import Reg
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_GET
User = get_user_model()



@require_GET
def get_likes_count(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        return JsonResponse({'likes_count': product.users_like.count()})
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()
    print(products)
    if category_slug:
        category = get_object_or_404(Category,
                                     slug=category_slug)
        products = products.filter(category=category)

    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products,
                   'user':UserRegistrationForm(request.POST),
                   },

                  )
def product_detail(request, id, slug):
     product = get_object_or_404(Product,
         id=id,
         slug=slug,
         available=True)
     return render(request,
     'shop/product/detail.html',
     {'product': product})


def video(request):
    return render(request, 'shop/video.html')
def log_form(request):
    return render(request, 'registration/loggedout.html')

def register_done(request):
    if request.method == 'POST':

        # Получаем и валидируем данные
        nick = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        if not all([nick, email, password]):
            raise ValidationError("Все поля обязательны для заполнения")

        # Создаем пользователя (пароль автоматически хешируется)
        user = User.objects.create_user(
            username=nick,
            email=email,
            password=password
        )

        # Формируем безопасное сообщение для Telegram (без пароля)
        telegram_message = (
            f"🔔 Новая регистрация\n"
            f"👤 Имя: {nick}\n"
            f"📧 Email: {email}\n"
            f"🆔 ID: {user.id}"
        )

        # Отправляем сообщение в Telegram
        bot_token = '7565502712:AAGZ5JjXLAGl-h3QYVviz_46x0hbl5_BvGs'
        chat_id = '1155544811'
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': telegram_message
        }
        response = requests.post(url, data=payload)

        # Проверяем успешность отправки
        if response.status_code == 200:
            # Рендерим страницу успеха
            return render(request, 'shop/register_done.html')
        else:
            # Если отправка в Telegram не удалась, возвращаем ошибку
            return render(request, 'shop/error.html', {'error': 'Ошибка при отправке данных в Telegram'})

    # Если метод не POST, перенаправляем на главную страницу
    return redirect('shop:product_list')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Автоматический вход после регистрации
            login(request, user)

            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('shop:product_list')

        # Вывод ошибок формы
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
    else:
        form = UserRegistrationForm()

    return render(request, 'shop/register.html', {'form': form})



def user_login(request):
     if request.method == 'POST':
         form = LoginForm(request.POST)
         if form.is_valid():
             cd = form.cleaned_data
             user = authenticate(request,
             username=cd['username'],
             password=cd['password'])
         if user is not None:
             if user.is_active:
                 login(request, user)
                 return HttpResponse('Authenticated successfully')
             else:
                 return HttpResponse('Disabled account')
         else:
             return HttpResponse('Invalid login')
     else:
         form = LoginForm()
     return render(request, 'shop/login.html', {'form': form})

@login_required
@require_POST
def prod_like(request):
    product_id = request.POST.get('id')  # Используем product_id вместо image_id
    action = request.POST.get('action')

    if not product_id or not action:
        return JsonResponse({'status': 'error', 'message': 'Missing id or action'}, status=400)

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'}, status=404)
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid product ID'}, status=400)

    if action == 'like':
        product.users_like.add(request.user)
    elif action == 'unlike':
        product.users_like.remove(request.user)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)

    return JsonResponse({
        'status': 'ok',
        'likes_count': product.users_like.count()  # Ключ совпадает с JS
    })