'''
Created on 13 sept. 2017

@author: chris
'''

from . import resource_module as res
from networkx import DiGraph, Graph, shortest_path
import ply.lex as lex
import ply.yacc as yacc


def make_name_d3compliant(s):
    if '-' in s:
        s0 = s.replace('-', '_')
        return s0
    else:
        return s


class Model():
    '''
    classdocs
    '''
    def __init__(self, modelName):
        '''
        Constructor
        '''
        self.name = modelName
        self.directed_net = DiGraph()
        self.undirected_net = Graph()
        self.directed_net.name = modelName
        self.undirected_net.name = modelName

    def createNode(self, host_name, neighbor_name):
        # creation des LRU comme node et des link comme edge
        host = res.LRU(host_name)
        neighbor = res.LRU(neighbor_name)
    # creation des ressource LINK dans les deux sens
        res.Link(host, neighbor)
        res.Link(neighbor, host)
    # creation du graohe dirigé
        self.directed_net.add_node(host.name)
        self.directed_net.add_node(neighbor.name)
        self.directed_net.add_edge(host.name, neighbor.name)
    # creation du graphe non dirigé
        self.undirected_net.add_node(host.name)
        self.undirected_net.add_node(neighbor.name)
    # creation d'un edge dirigé host->neighbor
        self.undirected_net.add_edge(host.name, neighbor.name)

    def readCSV(self, neighborLinkFilename, data_directory):
        # structure du ficher csv
        # hostname, neighbor_name, hostPortId, neighborPortId
        file_name = neighborLinkFilename[0]
        file_ext = neighborLinkFilename[-1]

        neighbor_link_file = data_directory + file_name+'.'+file_ext
        nf = open(neighbor_link_file)
        nf_lines = nf.readlines()[1:]

        # on genere un graphe sur les indications host->neighbor

        for record in nf_lines:
            host_name = record.split(',')[0]
            neighbor_name = record.split(',')[1]

            self.createNode(host_name, neighbor_name)

    def readDAT(self, neighborLinkFilename, data_directory):
        file_name = neighborLinkFilename[0]
        file_ext = neighborLinkFilename[-1]

        neighbor_link_file = data_directory + file_name+'.'+file_ext
        nf = open(neighbor_link_file)
        nf_lines = nf.read()
        ######################################################################
        # definition de tokens
        ######################################################################
        tokens = (
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

        reserved = {'hostname': 'HOSTNAME',
                    'neighborName': 'NEIGHBORNAME',
                    'hostPortId': 'HOSTPORT',
                    'neighborPortId': 'NEIGHBORPORT'}

        t_COMMENT = r'\#(.)*'
        # def t_COMMENT(t):
        #     r'\#(.)*'
        #     pass
        t_COMMA = r','
        t_SEMICOLON = r';'
        t_EQUAL = r'='

        def t_LRUID(t):
            r'[a-zA-Z_][a-zA-Z_0-9-]*'
            t.type = reserved.get(t.value, 'LRUID')
            return t

        def t_NUMBER(t):
            r'\d+'
            t.value = int(t.value)
            return t

        def t_newline(t):
            r'\n+'
            t.lexer.lineno += len(t.value)

        t_ignore  = ' \t\"'

        def t_error(t):
            print("Illegal character '%s'" % t.value[0])
            t.lexer.skip(1)

        # Build the lexer
        lexer = lex.lex()
        ###########################################################
        # Give the lexer some input
        # utile pour tester le fonctionnement du lexer
        lexer.input(nf_lines)
        while True:
            tok = lexer.token()
            if not tok:
                break      # No more input
            print(tok)
        ############################################################
        # definition des regles de parsing
        ###########################################

        def p_block(p):
            '''block  : block monitoring
                      | block comment
                      | monitoring
                      | comment'''
            pass

        def p_comment(p):
            '''comment : COMMENT'''
            pass

        def p_monitoring(p):
            '''monitoring : id_host COMMA id_neighbor COMMA id_hostPort COMMA id_neighborPort SEMICOLON'''
            p[0] = list(p[i] for i in range(len(p)))   # pour tester le parser
            print(p[0])                                # pour tester le parser
            self.createNode(p[1], p[3])

        def p_id_host(p):
            '''id_host : HOSTNAME EQUAL LRUID '''
            p[0] = make_name_d3compliant(p[3])
            pass

        def p_id_neighbor(p):
            '''id_neighbor : NEIGHBORNAME EQUAL LRUID '''
            p[0] = make_name_d3compliant(p[3])
            pass

        def p_id_hostPort(p):
            '''id_hostPort : HOSTPORT EQUAL NUMBER '''
            p[0] = p[3]

        def p_id_neighborPort(p):
            '''id_neighborPort : NEIGHBORPORT EQUAL NUMBER'''
            p[0] = p[3]

        # Error rule for syntax errors
        def p_error(p):
            print("Syntax error in input!" + str(p))

        # Build the parser
        parser = yacc.yacc(debug=1)
        s = nf_lines
        result = parser.parse(s)
        print('result: ', result)

    def getshortestPathWithLink(self, source_LRU, target_LRU):
        path = shortest_path(self.undirected_net,
                             source_LRU.name, target_LRU.name)
        res_dict = res.resource_dict
        full_path = []
        i = 0
        while i < len(path)-1:
            end1 = path[i]
            full_path += [res_dict[end1]]
            i = i + 1
            end2 = path[i]
            link = res.giveLinkName(res_dict[end1], res_dict[end2])
            full_path += [res_dict[link]]
        full_path += [res_dict[end2]]
        return full_path
