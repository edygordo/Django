from django.urls import reverse,include,path
from .views import CreateUserView, CreateTokenView, ManageUserView

app_name='user'
urlpatterns=[
    path('create/',view=CreateUserView.as_view(),name='create'),
    path('token/',view=CreateTokenView.as_view(), name='token'),
    path('me/',view=ManageUserView.as_view(),name='me')
]