# coding = utf-8
import mysql.connector


def login_sql():
    conn = mysql.connector.connect(user='root', password='admin', database='test')
    return conn

def ip2int(ip):
    try:
        # % X表示输出16进制形式，使用A～F的大写字符，比如15就输出F
        # % 02 X表示输出的16进制使用两个位置，如果只有一位的前面添0，比如15就输出0F
        hexn = ''.join(["%02X" % int(i) for i in ip.split('.')])

    except BaseException:
        hexn = ''.join(["%02X" % int(i) for i in '0.0.0.0'.split('.')])
    return int(hexn, 16)
    #轮子
    # import struct,socket
    # return struct.unpack("!I",socket.inet_aton(ip))[0]


def int2ip(n):
    d = 256 * 256 * 256
    q = []
    while d > 0:
        # 把除数和余数运算结果结合起来，返回一个包含商和余数的元组
        m, n = divmod(n, d)
        q.append(str(m))
        d = d / 256
    return '.'.join(q)
    # 轮子
    # import socket, struct
    # return socket.inet_ntoa(struct.pack("!I", n))

def insert_row():
    conn = mysql.connector.connect(user='root', password='admin', database='test')
    # 指定编码格式
    with open('./ipdata.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nl_p_list = []
    for l in lines:
        # 指定切割次数，并将数据中的空格删除
        ls = l.strip().split(',', 4)
        # print(l)
        # print(*ls)
        # assert len(ls) == 5
        c1, c2, c3, c4, c5 = ls[0], ip2int(ls[1]), ip2int(ls[2]), ls[3], ls[4]
        nl = [c1, c2, c3, c4, c5]
        nl_p_list.append(nl)
        # print(nl)
    # 连接数据数据库游标
    cursor = conn.cursor()
    # ret = cursor.executemany('insert into ipdata (id, startip, endip, country, carrier) values (%s, %s, %s, %s, %s)',
    #                          nl_p_list)

    for i in range(int(len(nl_p_list) / 1000 + 1)):
        tmp_nl_p_list = nl_p_list[i * 1000: (i + 1) * 1000]
        # print(tmp_nl_p_list[i][0] + ': ' + tmp_nl_p_list[i][4])
        # 批量插入表中
        ret = cursor.executemany(
            'insert into ipdata (id, startip, endip, country, carrier) values (%s, %s, %s, %s, %s)',
            tmp_nl_p_list)
    # 提交事务;关闭数据库连接
    conn.commit()
    conn.close()




if __name__ == '__main__':

    # print(ip2int('127.0.0.1'))
    # print("%02X" % int(126))
    # print(int('0', 16))
    # print(int2ip(ip2int('127.0.0.1')))
    with open('./ipdata.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nl_p_list = []
    for l in lines:
        ls = l.strip().split(',', 4)
        c1, c2, c3, c4, c5 = ls[0], ip2int(ls[1]), ip2int(ls[2]), ls[3], ls[4]
        nl = [c1, c2, c3, c4, c5]
        nl_p_list.append(nl)

    import random
    import time

    ip_list = list(map(lambda x: x[1], random.sample(nl_p_list, 100)))
    conn = login_sql()
    #避免 mysql.connector InternalError: Unread result found 错误， 添加参数
    cursor = conn.cursor(buffered=True)
    # cursor.execute('SELECT * FROM ipdata WHERE 1780997668 BETWEEN startip AND endip')
    ret_list = []
    sql_list = []
    sql_list2 = []
    sql_str = 'SELECT {0}.* FROM (SELECT * FROM ipdata WHERE %s >=  startip ORDER BY startip DESC  LIMIT 1) {0}'
    sql_str2 = 'SELECT {0}.* FROM (SELECT * FROM ipdata WHERE %s BETWEEN startip AND endip) {0}'

    for i in range(len(ip_list)):
        sql_list.append(sql_str.format('t' + str(i)) % ip_list[i])
        sql_list2.append(sql_str2.format('t' + str(i)) % ip_list[i])
    # for i in range(len(sql_list)):
    #     print(sql_list[i])

    # 拼接 SQL 语句
    sql = ' union all '.join(sql_list)
    sql2 = ' union all '.join(sql_list2)

    # zip() 函数接受任意多个（包括0个和1个）序列作为参数，返回一个tuple列表
    # dict() 函数是从可迭代对象来创建新字典。比如一个元组组成的列表



    # print(sql)
    t0 = time.time()
    # dict(zip(ip_list, cursor.execute(sql)))
    cursor.execute(sql)

    t1 = time.time()
    # for i in ip_list:
    #     cursor.execute('SELECT * FROM ipdata WHERE %s >=  startip ORDER BY startip DESC LIMIT 1' % i)
    #     result = cursor.fetchall()
        # startip, endip = result[0][1], result[0][2]
        # if startip <= i <= endip:
        #     ret_list.append((i, result[0][3]))
        # else:
        #     ret_list.append((i, u'unknown'))
        # print(result[0][1]+ ' str ' + result[0][2])
    t2 = time.time()

    # for i in ip_list:
    #     cursor.execute('SELECT * FROM ipdata WHERE %s BETWEEN startip AND endip' % i)
    #     result = cursor.fetchall()

    t3 = time.time()
    # cursor.execute(sql2)
    t4 = time.time()

    print(t1 - t0)
    print(t2 - t1)
    print(t4 - t3)
    print(t3 - t2)

    cursor.close()
    conn.close()



