"""Minimal Ethereum node representation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from ..node import AbstractNode
from .rpc import EthereumRPC


@dataclass
class EthereumNode(AbstractNode):
    """A lightweight :class:`~cryptoadvance.specter.node.AbstractNode` implementation
    for Ethereum networks.

    Only a subset of :class:`AbstractNode` functionality is implemented; methods
    unrelated to Ethereum are intentionally minimal.
    """

    url: str = "http://localhost:8545"
    chain_id: int = 1
    _rpc: Optional[EthereumRPC] = None

    def update_rpc(self) -> None:
        self._rpc = EthereumRPC(self.url)

    @property
    def rpc(self) -> EthereumRPC:
        if self._rpc is None:
            self.update_rpc()
        return self._rpc

    def node_info_template(self) -> str:
        """Return path to an Ethereum specific node info template."""
        return "node/components/ethereum_node_info.jinja"
