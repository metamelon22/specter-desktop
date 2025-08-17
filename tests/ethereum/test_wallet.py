import pytest

web3 = pytest.importorskip("web3")

from web3 import EthereumTesterProvider
from cryptoadvance.specter.ethereum.rpc import EthereumRPC
from cryptoadvance.specter.ethereum.wallet import EthereumWallet


def test_send_transaction():
    provider = EthereumTesterProvider()
    rpc = EthereumRPC(provider=provider)
    tester = provider.ethereum_tester
    acct0, acct1 = tester.get_accounts()[:2]
    key = tester.backend.account_keys[0].to_hex()
    wallet = EthereumWallet(rpc, key)
    tx = wallet.create_transaction(to=acct1, value=1, chain_id=tester.get_chain_id())
    raw = wallet.sign_transaction(tx)
    tx_hash = wallet.send_transaction(raw)
    receipt = rpc.get_transaction_receipt(tx_hash)
    assert receipt["status"] == 1
