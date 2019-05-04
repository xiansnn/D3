'''
Created on 30 sept. 2017

@author: chris
'''
from modelizer import DAT_parser as dp
from modelizer import modelGenerator as mg

data_directory = r"C:\Users\chris\OneDrive\Liclipse\D3Converter\datafiles" 
n_file_name = r"\A321S_neighborlink.dat"
model = mg.Model('test') 
maintenance_server_name = 'DSU1'

neighbor_link_file = data_directory + n_file_name
nf = open(neighbor_link_file)
nf_lines = nf.read()
lex = dp.DAT_lexer()
lex.build()
lex.test(nf_lines)
pars = dp.DAT_parser()
pars.build()
pars.parse(nf_lines, lex.lexer)
pass
print('end')