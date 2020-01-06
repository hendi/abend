"""blockchain_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from blockchain.views import Mint, TransferAeter, GetNonce, GetBalance, GetTransferTx, BroadcastSignedTx

urlpatterns = [
    path('admin/', admin.site.urls),

    # blockchain
    path("blockchain/mint", Mint.as_view()),
    path("blockchain/transfer_aeter", TransferAeter.as_view()),
    path("blockchain/get_nonce", GetNonce.as_view()),
    path("blockchain/get_balance", GetBalance.as_view()),
    path("blockchain/get_transfer_tx", GetTransferTx.as_view()),
    path("blockchain/broadcast_signed_tx", BroadcastSignedTx.as_view()),
]
