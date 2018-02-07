# coding = utf-8
import mysql.connector


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

conn = mysql.connector.connect(user='root', password='admin', database='test')



if __name__ == '__main__':
    # print(ip2int('127.0.0.1'))
    # print("%02X" % int(126))
    # print(int('0', 16))
    # print(int2ip(ip2int('127.0.0.1')))

    #指定编码格式
    with open('./ipdata.csv', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    nl_p_list = []
    for l in lines:
        #指定切割次数，并将数据中的空格删除
        ls = l.strip().split(',', 4)
        # print(l)
        # print(*ls)
        # assert len(ls) == 5
        c1, c2, c3, c4, c5 = ls[0], ip2int(ls[1]), ip2int(ls[2]), ls[3], ls[4]
        nl = [c1, c2, c3, c4, c5]
        nl_p_list.append(nl)
        # print(nl)
    #连接数据数据库游标
    cursor = conn.cursor()

    for i in range(int(len(nl_p_list)/1000 +1)):
        tmp_nl_p_list = nl_p_list[i*1000: (i+1)*1000]
        # print(tmp_nl_p_list[i][0] + ': ' + tmp_nl_p_list[i][4])
        # 批量插入表中
        ret = cursor.executemany('insert into ipdata (id, startip, endip, country, carrier) values (%s, %s, %s, %s, %s)',
                       tmp_nl_p_list)
    # 提交事务;关闭数据库连接
    conn.commit()
    conn.close()