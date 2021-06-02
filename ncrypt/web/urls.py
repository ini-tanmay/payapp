from django.urls import include,path
from .views import *

urlpatterns = [
    path('create/<str:secret>',create_account),
    path('token_balance/<str:address>/token/<str:token_address>',token_balance),
    path('eth_balance/<str:address>',ether_balance),
    path('transfer/<str:address>/to/<str:to_address>/token/<str:token_address>',transfer_money),
]
