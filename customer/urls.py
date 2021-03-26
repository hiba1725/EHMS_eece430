from django.urls import path

from . import views

app_name = 'customer'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('account/', views.account_info, name='account_info'),
    path('add_card/', views.add_card, name='add_card'),
    path('remove_card/', views.remove_card, name='remove_card'),
    path('edit_account_info/', views.edit_account_info, name='edit_account_info'),
    # path('<int:question_id>/', views.detail, name='detail'),
    # path('<int:question_id>/results/', views.results, name='results'),
    # path('<int:question_id>/vote/', views.vote, name='vote')
]