#!/usr/bin/env python
# -*- coding: utf-8 -*-


import ssl
import OpenSSL
from dateutil import parser
from queue import Queue
from multiprocessing import Pool
import csv


task_queue = Queue()
crt_info = []
process_num = 50


def setcallback(msg):
    print(msg)
    crt_info.append(msg)


def get_expire_time(ip_port, index):
    hostname, port = ip_port.split(':')
    url = 'https://{}'.format(ip_port)
    try:
        cert = ssl.get_server_certificate((hostname, port)).encode()
        cert_obj = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        # 获取证书的起、止时间，及是否过期
        not_before = parser.parse(cert_obj.get_notBefore().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S')
        not_after = parser.parse(cert_obj.get_notAfter().decode("UTF-8")).strftime('%Y-%m-%d %H:%M:%S')
        has_expired = cert_obj.has_expired()

        # 获取 issue_to 和 issuer 信息
        subject = cert_obj.get_subject()
        issued_to = subject.CN  # the Common Name field
        issuer = cert_obj.get_issuer()
        issued_by = issuer.CN

        column = [index, hostname, port, url, not_before, not_after, has_expired, issued_to, issued_by, '-']
    except Exception as e:
        column = [index, hostname, port, url, '-', '-', '-', '-', '-', e]
    finally:
        return column


def run_crt_check():
    pool = Pool(process_num)  # 创建进程池
    index = 0
    while not task_queue.empty():
        index += 1
        host_port = task_queue.get(timeout=1.0)
        pool.apply_async(get_expire_time, args=(host_port, index), callback=setcallback)
    pool.close()
    pool.join()


def load_targets():
    target_file = './target_file.txt'
    global task_queue
    with open(target_file, 'r') as fr:
        for line in fr:
            host_port = line.strip()
            task_queue.put(host_port)


def save_2_csv():
    with open("crt_info.csv", "w", encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        # 先写入columns_name
        writer.writerow(["编号", "主机", "端口", "URL", "开始时间", "过期时间", "是否过期", "签发给", "签发者", "备注"])
        global crt_info
        for line in crt_info:
            writer.writerow(line)
    pass


if __name__ == '__main__':
    # 读取文件中的检测目标到任务队列中
    load_targets()
    # 检查证书的过期时间
    run_crt_check()
    #  保存数据到文件中
    save_2_csv()
