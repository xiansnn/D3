'''
Created on 10 sept. 2017

@author: chris
'''
import modelizer.DSL_generator as dsl
import modelizer.resource_module as res
from modelizer import service_module as srv

# import des parametres d'initialisation
from . import *


if __name__ == '__main__':

    neighbor_link_file_name = n_file_name.split(sep='.')
    file_extension = neighbor_link_file_name[-1]

    if file_extension == 'csv':
        model.readCSV(neighbor_link_file_name, data_directory)
    elif file_extension == 'dat':
        model.readDAT(neighbor_link_file_name, data_directory)
    # creation des services
    full_monitoring_coverage = True
    srv.ALIVEserviceGenerator(model, all_neighbor=full_monitoring_coverage)
    srv.MIDserviceGenerator(model, maintenance_server_name)
    srv.LINKserviceGenerator(model, maintenance_server_name)

    # creation des fichiers DSL
    if full_monitoring_coverage:
        D3file_name = '\\' + model.name + '_fullMonit'
    else:
        D3file_name = '\\' + model.name + '_halfMonit'

    dsl.createDSLfile(D3file_name, data_directory)

    print('nb resource = ' + str(len(res.resource_dict)))
    print('total nb of services = ' + str(len(srv.service_dict)))
    print('end')
