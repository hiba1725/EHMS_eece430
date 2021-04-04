from django.urls import path

from . import views

app_name = 'doctor'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit_account_info/', views.edit_account_info, name='edit_account_info'),
    path('edit_password/', views.edit_password, name='edit_password'),
    path('search_doctors/', views.DoctorSearch.as_view(), name="dsearch"),
    path('list_doctors/', views.DoctorSearchResult.as_view(), name="dlist"),
    # path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote')
]