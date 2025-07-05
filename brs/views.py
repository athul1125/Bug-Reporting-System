from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLogoutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'logout.html')
    
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)
        return render(request, 'logout.html')
