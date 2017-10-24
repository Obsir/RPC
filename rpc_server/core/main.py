# @Time    : 2017/10/24 上午11:24
# @Author  : Obser


from core import rpc_server


def run():
    server = rpc_server.RpcServer()
    server.start()