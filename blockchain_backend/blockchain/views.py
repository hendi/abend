# TODO
# catch all exceptions, return error
# pythonh: exception.backtrace to string

import json

from django.views.generic import View
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .blockchain import Blockchain
from .models import APILog, Account


class Mint(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        bc = Blockchain()

        _tx, call_obj = bc.mint(request.POST["receiver_pubkey"], request.POST["amount"])

        if call_obj.return_type == "ok":
            ret = json.dumps({"status": "ok"})
        else:
            ret = json.dumps({
                "status": "error",
                "reason": bc.compiler.decode_data("string", call_obj.return_value),
            })

        APILog.objects.create(method="Mint",
                              args=json.dumps({
                                  "receiver_pubkey": request.POST["receiver_pubkey"],
                                  "amount": request.POST["amount"],
                              }),
                              result=ret)

        return HttpResponse(ret)


class TransferAeter(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        bc = Blockchain()

        try:
            tx = bc.transfer_aeter(request.POST["receiver_pubkey"], request.POST["amount"])

            ret = json.dumps({
                "status": "ok",
                "tx_hash": tx.hash,
            })
            code = 200
        except Exception as e:
            ret = json.dumps({
                "status": "error",
                "reason": str(e),
            })
            code = 412

        APILog.objects.create(method="TransferAeter",
                              args=json.dumps({
                                  "receiver_pubkey": request.POST["receiver_pubkey"],
                                  "amount": request.POST["amount"],
                              }),
                              result=ret)

        return HttpResponse(ret, status=code)


class GetBalance(View):
    def get(self, request):
        bc = Blockchain()
        ret = bc.get_balance(request.GET["pubkey"])

        """
        APILog.objects.create(method="GetBalance",
                              args=json.dumps({
                                  "pubkey": request.GET["pubkey"],
                              }),
                              result=ret)
        """

        return HttpResponse(ret, status=200)


class GetNonce(View):
    def get(self, request):
        bc = Blockchain()
        ret = bc.get_nonce(request.GET["pubkey"])

        """
        APILog.objects.create(method="GetNonce",
                              args=json.dumps({
                                  "pubkey": request.GET["pubkey"],
                              }),
                              result=ret)
        """

        return HttpResponse(ret, status=200)


class GetTransferTx(View):
    def get(self, request):
        bc = Blockchain()
        tx = bc.create_call_tx(
            request.GET["caller_pubkey"],
            "transfer",
            [request.GET["receiver_pubkey"], request.GET["amount"]],
        )

        ret = json.dumps(tx.tx)

        APILog.objects.create(method="GetTransferTx",
                              args=json.dumps({
                                  "caller_pubkey": request.GET["caller_pubkey"],
                                  "receiver_pubkey": request.GET["receiver_pubkey"],
                                  "amount": request.GET["amount"],
                              }),
                              result=ret)

        return HttpResponse(ret, status=200)


class BroadcastSignedTx(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request):
        bc = Blockchain()
        tx_id = bc.broadcast_tx(request.POST["signed_tx"])

        call_obj = bc.contract.get_call_object(tx_id)

        if call_obj.return_type == "ok":
            ret = json.dumps({"status": "ok"})
            code = 200
        else:
            ret = json.dumps({
            "status": "error",
            "reason": bc.compiler.decode_data("string", call_obj.return_value),
            })
            code = 412

        APILog.objects.create(method="BroadcastSignedTx",
                              args=json.dumps({
                                  "signed_tx": request.POST["signed_tx"],
                              }),
                              result=ret)

        return HttpResponse(ret, status=code)
