#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/20 10:18
# @Author  : Lynn
# @Site    : 
# @File    : selector_to_xpath.py
# @Software: PyCharm

# _*_ coding:utf-8 _*_
import sys
import ply.lex as lex
import ply.yacc as yacc


class Parser(object):
    tokens = ()
    precedence = ()

    def __init__(self):
        lex.lex(module = self)
        yacc.yacc(module = self)

    def parse(self, str):
        return yacc.parse(str)


class Selector(Parser):
    literals = ['.', '#', '[', ']', '<', '>', '=', '+', ':', '(', ')', '*', '$', '^']
    tokens = (
        'NAME', 'VALUE', 'PARENT', 'COMMENT',
    )
    t_NAME = r'[a-zA-Z0-9_-]+'
    t_PARENT = r'<<'
    t_VALUE = r'=[^ \]]+'
    t_COMMENT = r'//.*'
    t_ignore = " \t"

    precedence = (
        ('nonassoc', 'NORMAL'),
        ('left', '[', '#', '.'),
        ('right', '+')
    )

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')

    def t_error(self, t):
        print('Illegal character "%s"' % t.value[0])
        t.lexer.skip(1)

    def p_result_1(self, p):
        'result : expression'
        p[0] = './/' + p[1]

    def p_result_2(self, p):
        'result : COMMENT'
        p[0] = p[1]

    def p_attr_1(self, p):
        'attr : "[" NAME "]"'
        p[0] = '@' + p[2]

    def p_attr_2(self, p):
        'attr : "[" NAME VALUE "]"'
        p[0] = '@%s="%s"' % (p[2], p[3][2:-1])

    def p_attr_3(self, p):
        'attr : "[" NAME VALUE "]" "[" NAME VALUE "]"'
        p[0] = '@%s="%s" and @%s="%s"' % (p[2], p[3][2:-1], p[6], p[7][2:-1])

    def p_attr_4(self, p):
        'attr : "[" NAME "*"  VALUE "]"'
        p[0] = 'contains(@%s, "%s")' % (p[2], p[4][2:-1])

    def p_attr_5(self, p):
        'attr : "[" NAME "^"  VALUE "]"'
        p[0] = 'starts-with(@%s, "%s")' % (p[2], p[4][3:-1])

    def p_attr_6(self, p):
        'attr : "[" NAME "$"  VALUE "]"'
        p[0] = 'ends-with(@%s, "%s")' % (p[2], p[4][2:-1])

    def p_attr_7(self, p):
        'attr : "#" NAME'
        p[0] = '@id="%s"' % p[2]

    def p_attr_8(self, p):
        'attr : "." NAME'
        p[0] = '@class="%s"' % p[2]

    def p_expr1(self, p):
        'expression : NAME attr'
        p[0] = '%s[%s]' % (p[1], p[2])

    def p_expr2(self, p):
        'expression : attr'
        p[0] = '*[%s]' % p[1]

    def p_expr3(self, p):
        'expression : "*" attr'
        p[0] = '*[%s]' % p[2]

    def p_expr4(self, p):
        'expression : NAME %prec NORMAL'
        p[0] = p[1]

    def p_expr5(self, p):
        'expression : expression expression %prec NORMAL'
        p[0] = '%s//%s' % (p[1], p[2])

    def p_expr6(self, p):
        'expression : expression ">" expression %prec NORMAL'
        p[0] = '%s/%s' % (p[1], p[3])

    def p_expr7(self, p):
        'expression : expression "<" %prec NORMAL'
        p[0] = '%s/..' % (p[1])

    def p_expr8(self, p):
        'expression : expression PARENT expression %prec NORMAL'
        p[0] = '%s/ancestor::%s' % (p[1], p[3])

    def p_expr9(self, p):
        'expression : expression "+" expression'
        p[0] = '/following-sibling::%s' % (p[3])

    def p_expr10(self, p):
        'expression : expression ":" NAME "(" expression ")" '
        if p[3] == 'nth-child':
            p[0] = '%s[%s]' % (p[1], p[5])

    def p_expr11(self, p):
        'expression : expression ":" NAME '
        if p[3] == 'first-child':
            p[0] = '%s[1]' % (p[1])
        elif p[3] == 'last-child':
            p[0] = '%s[last()]' % (p[1])

    def p_expr12(self, p):
        'expression : expression "^" "=" expression '
        p[0] = 'starts-with(@%s,%s)' % (p[1], p[4])

    def p_error(self, p):
        if p:
            print('Syntax error at "%s"' % p.value)
        else:
            print('Syntax error at EOF')


_selector = None

if _selector is None:
    _selector = Selector()


def selector(s):
    if s[:2] == '//':
        return s
    if s[:1] == '@':
        return s[1:]
    else:
        return _selector.parse(s)


if sys.version_info[0] >= 3:
    raw_input = input

if __name__ == '__main__':
    selector = Selector()
    while 1:
        try:
            s = raw_input('>>>')
        except:
            print('\r')
            break
        if not s:
            continue
        print(selector.parse(s))
