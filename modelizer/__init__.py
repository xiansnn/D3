# creation modele
import modelizer.modelGenerator as mg

# data_directory = r"C:\Users\chris\Dropbox\D3\d3\datafiles"
data_directory = r".\datafiles"

# n_file_name = r"\mini_cab_neighborlink.csv"
# n_file_name = r"\neighborlink.dat"D3\d
# n_file_name = r"\A319_neighborlink_gd.csv"
# n_file_name = r"\A319_neighborlink.dat"
n_file_name = r"\A321S_neighborlink.dat"

# model = mg.Model('A319')
model = mg.Model('A321S')
# model = mg.Model('mini_cab')

maintenance_server_name = 'DSU1'
