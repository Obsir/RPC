# @Time    : 2017/10/24 上午11:34
# @Author  : Obser

from core import rpc_client
import threading
import random


class RpcHandler(object):
    def __init__(self):
        self.task_dict = {}
        self.client_pool = {}

    def start(self):
        self.__interactive()

    def __interactive(self):
        """
        开启交互程序
        :return:
        """
        while True:
            cmd = input("请输入指令>>:").strip()
            if len(cmd) == 0:
                continue
            cmd_str = cmd.split()[0]
            if hasattr(self, "cmd_%s" % cmd_str):
                func = getattr(self, "cmd_%s" % cmd_str)
                func(cmd)
            else:
                self.cmd_call(cmd)

    def cmd_check(self, *args):
        """
        根据task_id查询响应
        :param args:
        :return:
        """
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            task_id = int(cmd_split[1])
            response = {}
            if task_id in self.task_dict:
                response = self.task_dict[task_id]["response"]
                client = self.task_dict[task_id]["client"]
                if client.done:
                    self.client_pool[client] = True
                    self.task_dict[task_id]["status"] = True
            print("\033[32;1mResponse:\033[0m")
            for ip in response:
                print("\033[34;1m[%s]:\033[0m\n\033[33;1m%s\033[0m" % (ip, response[ip]))

    def cmd_checkall(self, *args):
        """
        查询当前所有任务
        :param args:
        :return:
        """
        for task_id in self.task_dict:
            print("\033[32;1mtask_id:\033[0m \033[34;1m%s\033[0m" % task_id, end=" | ")
            if self.task_dict[task_id]["status"]:
                status = "\033[32;1mDone\033[0m"
            else:
                status = "\033[31;1mRunning or Waiting to be checked\033[0m"
            print("\033[33;1mstatus:\033[0m", status)

    def cmd_call(self, *args):
        """
        执行任务
        :param args:
        :return:
        """
        cmd_split = args[0].split()
        if len(cmd_split) > 1:
            for client in self.client_pool:
                if self.client_pool[client]:
                    new_client = client
                    break
            else:
                new_client = rpc_client.RpcClient()

            self.client_pool[new_client] = False
            task_id = random.randint(10000, 99999)
            threading.Thread(target=new_client.call, args=(cmd_split[0], cmd_split[1:])).start()
            self.task_dict[task_id] = {
                "client": new_client,
                "response": new_client.response,
                "status": False
            }
            print("[task_id]:", task_id)
