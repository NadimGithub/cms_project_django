from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, login_view, dashboard,forgotpassword,changepassword,ProfilePageView
urlpatterns = [
    path('register/', register, name='register'),
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),

    path('forgotpassword/',forgotpassword, name='forgotpassword'),
    path('changepassword/<token>/',changepassword, name='changepassword'),


    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_comfirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complate', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
