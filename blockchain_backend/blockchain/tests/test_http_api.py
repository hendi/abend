import json

from django.test import TestCase

from blockchain.blockchain import Blockchain


class BlockchainTest(TestCase):
    KEYS = [
        ("ak_zPoY7cSHy2wBKFsdWJGXM7LnSjVt6cn1TWBDdRBUMC7Tur2NQ", "36595b50bf097cd19423c40ee66b117ed15fc5ec03d8676796bdf32bc8fe367d82517293a0f82362eb4f93d0de77af5724fba64cbcf55542328bc173dbe13d33"),
        ("ak_gLYH5tAexTCvvQA6NpXksrkPJKCkLnB9MTDFTVCBuHNDJ3uZv", "6eb127925aa10d6d468630a0ca28ff5e1b8ad00db151fdcc4878362514d6ae865951b78cf5ef047cab42218e0d5a4020ad34821ca043c0f1febd27aaa87d5ed7"),
        ("ak_23p6pT7bajYMJRbnJ5BsbFUuYGX2PBoZAiiYcsrRHZ1BUY2zSF", "e15908673cda8a171ea31333538437460d9ca1d8ba2e61c31a9a3d01a8158c398a14cd12266e480f85cc1dc3239ed5cfa99f3d6955082446bebfe961449dc48b"),
    ]

    def setUp(self):
        self.bc = Blockchain()

    def test_mint(self):
        pubkey = self.KEYS[0][0]
        amount = int(1.234e8)

        balance_pre = self.bc.get_balance(pubkey)

        response = self.client.post("/blockchain/mint", {
            "receiver_pubkey": pubkey,
            "amount": amount,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["status"], "ok")

        balance_post = self.bc.get_balance(pubkey)

        self.assertEqual(balance_post, balance_pre + amount)

    def test_transfer_aeter(self):
        pubkey = self.KEYS[0][0]
        amount = int(1.234e8)

        balance_pre = self.bc.get_balance_aeter(pubkey)

        response = self.client.post("/blockchain/transfer_aeter", {
            "receiver_pubkey": pubkey,
            "amount": amount,
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content.decode("utf-8"))["status"], "ok")

        balance_post = self.bc.get_balance_aeter(pubkey)

        self.assertEqual(balance_post, balance_pre + amount)

    def test_get_balance(self):
        pubkey = self.KEYS[0][0]

        response = self.client.get("/blockchain/get_balance", {
            "pubkey": pubkey,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.decode("utf-8").isdigit())

    def test_get_nonce(self):
        pubkey = self.KEYS[0][0]

        response = self.client.get("/blockchain/get_nonce", {
            "pubkey": pubkey,
        })

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.decode("utf-8").isdigit())

    def test_get_transfer_tx(self):
        # TODO
        pass

    def test_broadcast_signed_tx(self):
        # TODO
        pass
