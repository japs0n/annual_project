#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from decimal import Decimal


class Calculator:
    def __init__(self, bill):
        self.bill = bill
        self.times = len(bill)
        self.top_record = bill[0]
        self.bus_times = 0
        self.bf_times = 0
        self.hosp_times = 0
        self.sum_price = Decimal()
        self.overdue_price = Decimal()
        self.overdue_times = 0
        self.type_list = dict()
        self.top_price = Decimal(self.top_record[5])
        for record in bill:
            if record[4] is None:
                continue
            hour = int(record[0][11:13])
            record_type = record[4].rstrip()
            price = Decimal(record[5])
            if price < self.top_price:
                self.top_record = record
            if hour in range(5, 9):
                self.bf_times += 1
            if price < 0:
                self.sum_price += price
            if record_type == '校医院':
                self.hosp_times += 1
            elif record_type == '车载收费':
                self.bus_times += 1
            elif record_type == '图书馆罚没款':
                self.overdue_times += 1
                self.overdue_price += price
            elif record_type not in ('开水器水控', '商贸一店好药师大药房', '新时代热水', '银行转账', '存款', '网费收缴（深澜）'):
                if record_type not in self.type_list:
                    self.type_list[record_type] = 0
                self.type_list[record_type] += 1

    def get_most_visit(self):
        high_visit = 0
        place = None
        for k, v in self.type_list.items():
            if v >= high_visit:
                place = k
                high_visit = v
        return place, high_visit

    def get_type_count(self):
        return len(self.type_list)
