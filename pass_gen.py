# -*- coding: utf-8 -*-
"""
Created on Sun Nov  7 15:18:23 2021

@author: Alex Akinin
"""

from random import choice as choice

engL = 'abcdefghijklmnopqrstuvwxyz'
engU = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# spec = '!"#$%&()*+-=?@[]~'
spec = '!#$%&()*+-=?@[~_'
numb = '0123456789'
alphs = [engL, engU, spec, numb]
confs = [True, True, True, True]

pass_len = 10


def gen_alph():
    alph = ''
    for i in range(len(confs)):
        if confs[i]:
            alph += alphs[i]
    return alph


def gen_password(alph, p_len=17):
    passw = ''
    for i in range(p_len):
        passw += choice(alph)
    return passw


password = [gen_password(gen_alph()) for _ in range(10)]

for i in range(len(password)):
    print(password[i])