"""Minimal Ethereum JSON-RPC client using web3.py."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

try:
    from web3 import Web3
except ImportError:  # pragma: no cover - handled in tests
    Web3 = None  # type: ignore


@dataclass
class EthereumRPC:
    """Light-weight wrapper around :mod:`web3` for a few common RPC calls.

    Parameters
    ----------
    provider_uri: str, optional
        HTTP provider URI. If not provided, ``provider`` must be passed.
    provider: Any, optional
        Instance of a ``web3`` provider. Useful for testing with
        :class:`web3.EthereumTesterProvider`.
    """

    provider_uri: Optional[str] = None
    provider: Optional[object] = None

    def __post_init__(self) -> None:
        if Web3 is None:  # pragma: no cover - defensive programming
            raise ImportError("web3 is required for EthereumRPC")
        if self.provider is not None:
            self.web3 = Web3(self.provider)
        else:
            uri = self.provider_uri or "http://localhost:8545"
            self.web3 = Web3(Web3.HTTPProvider(uri))

    def get_balance(self, address: str) -> int:
        """Return the balance for ``address`` in wei."""
        return self.web3.eth.get_balance(address)

    def get_transaction_count(self, address: str) -> int:
        """Return the nonce for ``address``."""
        return self.web3.eth.get_transaction_count(address)

    def send_raw_transaction(self, raw_tx: bytes) -> bytes:
        """Broadcast ``raw_tx`` to the network."""
        return self.web3.eth.send_raw_transaction(raw_tx)

    def get_transaction_receipt(self, tx_hash: bytes):
        """Fetch the transaction receipt for ``tx_hash``."""
        return self.web3.eth.get_transaction_receipt(tx_hash)
