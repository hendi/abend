from django.conf import settings

from aeternity import transactions, signing, node, identifiers, hashing, contract, defaults


class Blockchain:
    def __init__(self):
        self.ae = node.NodeClient(node.Config(
            external_url=settings.NODE_URL,
            network_id=settings.NETWORK_ID,
            native=True,
            debug=False,
        ))
        with open("../ae/contracts/AbendContract.aes") as fp:
            self.source = fp.read()

        self.compiler = contract.CompilerClient()

        self.contract = self.ae.Contract()
        self.contract.address = settings.CONTRACT

        self.acc_owner = signing.Account.from_secret_key_string(settings.OWNER_PK)
        deployed = self.ae.get_contract(pubkey=settings.CONTRACT)
        assert deployed.active is True
        assert deployed.owner_id == self.acc_owner.get_address()

    def mint(self, pubkey, amount):
        assert pubkey.startswith("ak_")
        assert int(amount) > 0

        return self.call_as_owner("mint", [pubkey, int(amount)])

    def transfer_aeter(self, pubkey, amount):
        assert pubkey.startswith("ak_")
        assert int(amount) > 0

        tx = self.ae.spend(self.acc_owner, pubkey, int(amount),
                           tx_ttl=0,
                           fee=0,
                           payload="",
        )

        # wait for a transaction to be included and confirmed
        #self.ae.wait_for_confirmation(tx.hash)
        # wait for a transaction to appear in the chain (no confirmations)
        self.ae.wait_for_transaction(tx.hash)

        return tx

    def get_balance_aeter(self, pubkey):
        assert pubkey.startswith("ak_")

        try:
            ret = self.ae.get_account_by_pubkey(pubkey=pubkey).balance
        except Exception as e:
            if "Account not found" in str(e):
                return 0

            raise e

        return ret

    def get_balance(self, pubkey):
        assert pubkey.startswith("ak_")

        (_tx, co) = self.call_as_owner("get_balance", [pubkey])
        return self.compiler.decode_data("int", co.return_value).data.value

    def get_nonce(self, pubkey):
        assert pubkey.startswith("ak_")

        return self.ae.get_next_nonce(pubkey)

    def call_as_owner(self, function, params):
        nonce_pre = self.ae.get_next_nonce(self.acc_owner.get_address())
        call_data = self.compiler.encode_calldata(self.source, function, params)

        tx = self.contract.call(settings.CONTRACT, self.acc_owner, function, params, call_data.calldata, gas=100000)
        self.ae.wait_for_transaction(tx.hash)

        nonce_post = self.ae.get_next_nonce(self.acc_owner.get_address())

        i = 0
        while nonce_post == nonce_pre and i < 3:
            nonce_post = self.ae.get_next_nonce(self.acc_owner.get_address())
            i += 1

        assert nonce_post > nonce_pre

        call_obj = self.contract.get_call_object(tx.hash)
        return (tx, call_obj)

    def create_call_tx(self, caller_pubkey, function, params):
        call_data = self.compiler.encode_calldata(self.source, function, params)

        vm_version, abi_version = self.ae.get_vm_abi_versions()

        tx_ttl = 0


        txb = self.ae.tx_builder
        nonce, ttl = self.ae._get_nonce_ttl(caller_pubkey, tx_ttl)

        tx = txb.tx_contract_call(caller_pubkey, settings.CONTRACT, call_data.calldata, function, params,
                                  0,  # amount
                                  100000,  # gas
                                  1000000000,  # gas_price
                                  abi_version,
                                  0,  # fee
                                  ttl, nonce)

        return tx

    def broadcast_tx(self, tx_signed):
        tx_id = self.ae.broadcast_transaction(tx_signed)
        self.ae.wait_for_transaction(tx_id)
        return tx_id
