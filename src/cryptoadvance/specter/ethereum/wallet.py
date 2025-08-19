"""Utilities for constructing and sending Ethereum transactions."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:
    from eth_account import Account
except ImportError:  # pragma: no cover - handled in tests
    Account = None  # type: ignore

from .rpc import EthereumRPC


@dataclass
class EthereumWallet:
    """Simple Ethereum wallet bound to a single private key."""

    rpc: EthereumRPC
    private_key: str

    def __post_init__(self) -> None:
        if Account is None:  # pragma: no cover - defensive
            raise ImportError("eth-account is required for EthereumWallet")
        self._account = Account.from_key(self.private_key)

    @property
    def address(self) -> str:
        return self._account.address

    def get_balance(self) -> int:
        return self.rpc.get_balance(self.address)

    def create_transaction(
        self,
        to: str,
        value: int,
        gas: int = 21_000,
        gas_price: Optional[int] = None,
        nonce: Optional[int] = None,
        chain_id: int = 1,
    ) -> dict:
        if gas_price is None:
            gas_price = self.rpc.web3.eth.gas_price
        if nonce is None:
            nonce = self.rpc.get_transaction_count(self.address)
        return {
            "to": to,
            "value": value,
            "gas": gas,
            "gasPrice": gas_price,
            "nonce": nonce,
            "chainId": chain_id,
        }

    def sign_transaction(self, tx: dict) -> bytes:
        signed = self._account.sign_transaction(tx)
        return signed.rawTransaction

    def send_transaction(self, raw_tx: bytes) -> bytes:
        return self.rpc.send_raw_transaction(raw_tx)
