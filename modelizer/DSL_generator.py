'''
Created on 18 sept. 2017

@author: chris
'''
from modelizer import service_module as srv
from . import resource_module as res


class createDSLfile():
    '''
    classdocs
    '''
    def __init__(self, file_name, data_directory):
        '''
        Constructor
        '''
        self.data_directory = data_directory
        self.file_name = file_name
        self.full_name = data_directory + file_name
        self.path_section = ''
        self.domain_section = ''
        self.resource_section = ''
        self.generateD3A()
        self.generateD3C()

    def generateD3A(self):
        # creation du fichier D3A
        for s in srv.service_dict:
            if s != "Communication":
                self.path_section += srv.service_dict[s].path_pattern
                # ecriture du fichier
        d3aFile = open(self.full_name+'.d3a', "w")
        d3aFile.write(self.path_section)
        d3aFile.close()

    def generateD3C(self):
        # creation du fichier D3C
        # section DOMAINS
        self.domain_section = 'DOMAINS\n'
        for d in srv.service_domain_dict:
            self.domain_section += '\t'
            + srv.service_domain_dict[d].declaration + '\n'
        self.domain_section += 'END\n\n'
        # section RESOURCES
        for r in res.resource_dict:
            resource = res.resource_dict[r]
            # declaration
            self.resource_section += resource.declaration
            # consumes service
            if len(resource.consumed_services) != 0:
                self.resource_section += '\tCONSUMES_SERVICE\n'
                s0 = ''
                for k in resource.consumed_services:
                    service = resource.consumed_services[k]
                    s0 += service.declaration
                self.resource_section += s0[:-2]+';\n'

            # provides service
            if len(resource.provided_services) != 0:
                self.resource_section += '\tPROVIDES_SERVICE\n'
                s0 = ''
                for k in resource.provided_services:
                    service = resource.provided_services[k]
                    s0 += service.declaration
                self.resource_section += s0[:-2]+';\n'
            # state transition
            self.resource_section += resource.state_trans_pattern

            # provides service dependence
            for k in resource.provided_services:
                service = resource.provided_services[k]
                self.resource_section += service.dependence
            pass
            self.resource_section += 'END\n\n'

# ecriture du fichier
        d3cFile = open(self.full_name + '.d3c', "w")
        d3cFile.write(self.domain_section)
        d3cFile.write(self.resource_section)
        d3cFile.close()