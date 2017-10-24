# @Time    : 2017/10/24 上午11:19
# @Author  : Obser


from core import rpc_handler


def run():
    handler = rpc_handler.RpcHandler()
    handler.start()
