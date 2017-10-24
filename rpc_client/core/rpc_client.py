# @Time    : 2017/10/24 上午11:20
# @Author  : Obser
from threading import Timer

import pika
import uuid
import time


class RpcClient(object):
    def __init__(self):
        self.response = {}
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.timer = Timer(10, self.reset)  # 设置延迟时间为15s
        self.channel.exchange_declare(exchange='direct_exchange',
                                      exchange_type='direct')

        self.channel.basic_consume(self.on_response,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        """
        回调函数
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        if self.corr_id == props.correlation_id:
            self.response[props.message_id] = body.decode()
            if len(self.response) == len(self.ips):
                self.done = True
                self.timer.cancel()
            else:
                self.done = False
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def reset(self):
        """
        请求时间超时，进行重置
        :return:
        """
        for ip in self.ips:
            if ip not in self.response:
                self.response[ip] = "\033[31;1mN/A\033[0m"
        self.done = True

    def call(self, cmd, ips):
        """
        执行命令
        :param cmd:
        :param ips:
        :return:
        """
        self.response.clear()
        self.corr_id = str(uuid.uuid4())
        self.done = False
        self.ips = ips
        if self.timer.is_alive():
            self.timer.cancel()
        self.timer = Timer(10, self.reset)
        for ip in ips:
            self.channel.basic_publish(exchange='direct_exchange',
                                       routing_key=ip,
                                       properties=pika.BasicProperties(
                                           reply_to=self.callback_queue,
                                           correlation_id=self.corr_id
                                       ),
                                       body=str(cmd))
        self.timer.start()
        while self.done is False:
            self.connection.process_data_events()  # 非阻塞版的start_consuming
