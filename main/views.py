# main/views.py
import json
import random

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from .models import Profile
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import GambleForm


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Замініть 'home' на вашу власну URL-шляху
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'main/login.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Перевірка чи профіль для цього користувача вже існує
            if not Profile.objects.filter(user=user).exists():
                Profile.objects.create(user=user)
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'main/register.html', {'form': form})

@login_required
def home(request):
    # Логіка вашого виду для домашньої сторінки
    return render(request, 'main/main.html')

@login_required
def profile(request):
    context = {
        'username': request.user.username,
        'points': request.user.profile.points,
        'miner_purchased': request.user.profile.miners > 0,
    }
    return render(request, 'main/profile.html', context)



@login_required
def buy_miner(request):
    if request.method == 'POST':
        profile = request.user.profile
        if profile.miners > 0:
            return JsonResponse({'error': 'Ви вже купили майнер'})
        if profile.points >= 4000:
            profile.points -= 4000
            profile.miners = 1
            profile.save()
            # Запланувати завдання для додавання балів кожну секунду
            return JsonResponse({'points': profile.points, 'miners': profile.miners})
        else:
            return JsonResponse({'error': 'Недостатньо монет'}, status=400)
    return JsonResponse({'error': 'Невідомий запит'}, status=400)

@login_required
def add_points(request):
    if request.method == 'POST':
        profile = request.user.profile
        profile.points += 100
        profile.save()
        return JsonResponse({'points': profile.points})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def gamble_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = GambleForm(request.POST)
        if form.is_valid():
            bet_amount = form.cleaned_data['bet_amount']
            if bet_amount > profile.points:
                messages.error(request, "Insufficient points")
            else:
                if random.choice([True, False]): # розібратись
                    profile.points += bet_amount
                    profile.save()
                    messages.success(request, f"You won {bet_amount} points! Your points have been doubled.") # з суксесами тоже
                else:
                    profile.points -= bet_amount
                    profile.save()
                    messages.error(request, "You lost! Better luck next time.")
            return redirect('gamble')
    else:
        form = GambleForm()

    context = {
        'form': form,
        'points': profile.points,
    }
    return render(request, 'main/gamble.html', context)