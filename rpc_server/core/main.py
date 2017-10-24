# @Time    : 2017/10/24 上午11:24
# @Author  : Obser


from core import rpc_server


def run():
    ip = input("请输入主机ip地址>>:")
    server = rpc_server.RpcServer(ip)
    server.start()