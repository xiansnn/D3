'''
Created on 30 sept. 2017

@author: chris
'''

import ply.lex as lex
import ply.yacc as yacc
from . import modelGenerator as mg
##############################################################################
# definition de tokens
##############################################################################


class DAT_lexer():
    def __init__(self):
        pass
        self.tokens = (
                'COMMENT',
                'LRUID',
                'NUMBER',
                'HOSTNAME',
                'NEIGHBORNAME',
                'HOSTPORT',
                'NEIGHBORPORT',
                'COMMA',
                'SEMICOLON',
                'EQUAL'
                )

        self.reserved = {'hostname': 'HOSTNAME',
                         'neighborName': 'NEIGHBORNAME',
                         'hostPortId': 'HOSTPORT',
                         'neighborPortId': 'NEIGHBORPORT'}

        self.t_COMMENT = r'\#(.)*'
        # def t_COMMENT(t):
        #     r'\#(.)*'
        #     pass
        self.t_COMMA = r','
        self.t_SEMICOLON = r';'
        self.t_EQUAL = r'='
        self.t_ignore = ' \t\"'

    def t_LRUID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9-]*'
        t.type = self.reserved.get(t.value, 'LRUID')
        return t

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


class DAT_parser():
    def __init__(self):
        pass
        ############################################################
        # definition des regles de parsing
        ###########################################

    def p_block(self, p):
        '''block  : block monitoring
                   | block comment
                   | monitoring
                   | comment'''
        pass

    def p_comment(self, p):
        '''comment : COMMENT'''
        pass

    def p_monitoring(self, p):
        '''monitoring : id_host COMMA id_neighbor
        COMMA id_hostPort COMMA id_neighborPort SEMICOLON'''
        p[0] = list(p[i] for i in range(len(p)))   # pour tester le parser
        print(p[0])                                # pour tester le parser
        self.createNode(p[1], p[3])

    def p_id_host(self, p):
        '''id_host : HOSTNAME EQUAL LRUID '''
        p[0] = mg.make_name_d3compliant(p[3])
        pass

    def p_id_neighbor(self, p):
        '''id_neighbor : NEIGHBORNAME EQUAL LRUID '''
        p[0] = mg.make_name_d3compliant(p[3])
        pass

    def p_id_hostPort(self, p):
        '''id_hostPort : HOSTPORT EQUAL NUMBER '''
        p[0] = p[3]

    def p_id_neighborPort(self, p):
        '''id_neighborPort : NEIGHBORPORT EQUAL NUMBER'''
        p[0] = p[3]

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input!" + str(p))

        # Build the parser
    def build(self):
        self.parser = yacc.yacc(debug=1)

    def parse(self, my_data, my_lexer):
        self.parser.parse(input=my_data, lexer=my_lexer)

#         s = nf_lines
#         result = parser.parse(s)
#         print('result: ', result)
