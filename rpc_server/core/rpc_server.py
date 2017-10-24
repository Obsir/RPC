# @Time    : 2017/10/24 上午11:24
# @Author  : Obser


# @Time    : 2017/10/20 上午12:06
# @Author  : Obser


import pika
import os


class RpcServer(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))

        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='rpc_queue')

    def on_request(self, ch, method, props, body):
        """
        处理命令
        :param ch:
        :param method:
        :param props:
        :param body:
        :return:
        """
        cmd = body.decode()

        print(" [.] cmd : %s" % cmd)
        try:
            response = os.popen(cmd).read()
        except Exception as e:
            response = e

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= \
                                                             props.correlation_id),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        """
        开启服务器
        :return:
        """
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue='rpc_queue')

        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

