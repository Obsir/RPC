# @Time    : 2017/10/24 上午11:24
# @Author  : Obser


# @Time    : 2017/10/20 上午12:06
# @Author  : Obser


import pika
import os


class RpcServer(object):
    def __init__(self, ip):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.ip = ip
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange="direct_exchange", exchange_type="direct")
        result = self.channel.queue_declare(exclusive=True)
        self.queue_name = result.method.queue
        self.channel.queue_bind(exchange='direct_exchange',
                                queue=self.queue_name,
                                routing_key=ip)

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
                         properties=pika.BasicProperties(correlation_id=props.correlation_id, message_id=self.ip),
                         body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        """
        开启服务器
        :return:
        """
        self.channel.basic_consume(self.on_request, queue=self.queue_name)
        print(" [%s] Awaiting RPC requests" % self.ip)
        self.channel.start_consuming()
