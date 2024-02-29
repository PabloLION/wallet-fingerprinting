from typing import TYPE_CHECKING, Any, cast

import matplotlib.pyplot as plt

from fingerprinting import analyze_block
from mempool_space import MempoolSpace
from type import WalletAnalyzeResult

if TYPE_CHECKING:
    plt = cast(Any, plt)  # plt has no stubs


ms = MempoolSpace()


def create_graph(block_height: int) -> WalletAnalyzeResult:
    wallet_info = WalletAnalyzeResult()
    blocks = ms.getblocks(block_height)

    for block in blocks:
        block_wallet_analyse_result = analyze_block(block)
        # TODO: add a to_readable_format method to WalletAnalyzeEntry
        for key in list(wallet_info.keys()):
            wallet_info[key]["total"] += block_wallet_analyse_result[key]["total"]
            wallet_info[key]["txs"] += block_wallet_analyse_result[key]["txs"]
    return wallet_info


def plot_graph(wallet_info: WalletAnalyzeResult):
    wallets = [wallet.value for wallet in wallet_info.keys()]
    wallet_tx_count = [wi["total"] for wi in wallet_info.values()]

    plt.figure(figsize=(10, 5))  # width:10, height:5
    plt.bar(wallets, wallet_tx_count, color="purple", width=0.5)
    plt.xlabel("Wallets")
    plt.ylabel("Number of Transactions")
    plt.show()


if __name__ == "__main__":
    create_graph(807038)
