#!/usr/bin/env python
# -*- coding: utf-8 -*
#
#
# class A(object):
#     __cls_name = 'A'
#     def __init__(self, name):
#         self.__x = name
#
#     def __foo(self):
#         print 'this is A.foo'
#
#     def bar(self):
#         self.foo()
#
#     # def __dir__(self):
#     #     return []
#
# class B(A):
#     __cls_name = 'B'
#     def foo(self):
#         print 'this is B.foo'
#         self._A__foo()
#
#
# #
# b = B(name='Bname')
# # a = A(name='Aname')
# # b.bar()
# b.foo()

import MySQLdb
from contextlib import contextmanager


@contextmanager
def get_connect():
    Con = MySQLdb.connect(host='192.168.0.201', user='root', passwd='eShiDai@1301', db='yestar_dev')
    cursor = Con.cursor()
    yield cursor
    cursor.close()
    Con.close()


@contextmanager
def get_file(file_name):
    f = open(file_name, 'w')
    yield f
    f.close()


def execute(sql):
    cursor.execute(sql)


def tables_gen(c):
    for table in c.fetchall():
        yield table[0]


with get_connect() as cursor, \
        get_file('database.txt') as f:
    execute("show tables")
    tables = []
    for t in tables_gen(cursor):
        # 取到表
        tables.append(t)
        execute("show columns from " + t)
        fields = cursor.fetchall()
        hr = ''
        col_lens = []
        col_len = []
        for y in xrange(6):
            col_len.append(6)
            for x in xrange(len(fields)):
                if fields[x][y] is not None:
                    col_len[y] = len(fields[x][y]) if col_len[y] < len(fields[x][y]) else col_len[y]
                else:
                    col_len[y] = 4
                if y == 4 and col_len[y] < 6:
                    col_len[y] = 8
            col_lens.append(col_len[y]+2)

        for c_len in col_lens:
            hr += '+' + "-"*c_len
        hr += '+'
        header = t + '\n' + hr + '\n' + \
                 '| Field' + ' '*(col_lens[0]-6) + \
                 '| Type' + ' '*(col_lens[1]-5) + \
                 '| Null' + ' '*(col_lens[2]-5) + \
                 '| Key' + ' '*(col_lens[3]-4) + \
                 '| Default' + ' '*(col_lens[4]-8) + \
                 '| Extra' + ' '*(col_lens[5]-7) + ' |' + \
                 '\n' + hr + '\n'
        body = ''
        for field in fields:
            field = [str(fie) for fie in field]
            body += '| ' + field[0] + ' '*(col_lens[0]-len(field[0])-1) + \
                    '| ' + field[1] + ' '*(col_lens[1]-len(field[1])-1) + \
                    '| ' + field[2] + ' '*(col_lens[2]-len(field[2])-1) + \
                    '| ' + field[3] + ' '*(col_lens[3]-len(field[3])-1) + \
                    '| ' + field[4] + ' '*(col_lens[4]-len(field[4])-1) + \
                    '| ' + field[5] + ' '*(col_lens[5]-len(field[5])-1) + '|\n'
        body += hr + '\n\n\n'
        data = header+body
        f.write(data)

