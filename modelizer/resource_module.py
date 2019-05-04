'''
Created on 10 sept. 2017

@author: chris
'''

from . import service_module as srv


resource_dict = {}


def giveLinkName(end1, end2):
    return "L_" + end1.name + "_" + end2.name


class Resource():
    '''
    classdocs
    '''
    def __init__(self, name):
        '''
        Constructor
        '''
        self.name = name
        self.is_communicant = False
        self.provided_services = {}
        self.consumed_services = {}
        self.resource_type = ''
        # on enregistre la nouvelle resource dans resource_dict
        resource_dict[self.name] = self
        # create resource + state declaration
        self.declaration = 'RESOURCE ' + self.name + '{OK,KO}\n'
        # create state and transition pattern
        s0 = ''
        s0 += '\n\tINITIAL OK;\n'
        s0 += '\tFAULTY KO;\n'
        s0 += '\tTRANS\n'
        s0 += '\t\tOK -> KO WHENEVER;\n\n'
        self.state_trans_pattern = s0

    def __repr__(self):
        return 'RES<'+self.name+'>'


class LRU(Resource):
    def __init__(self, name):
        super().__init__(name)
        self.resource_type = 'LRU'
        # ajout de variables utiles pour le service ALIVE
        self.ALIVE_service = {}
        self.monitoring_host = {}

    def is_communicant(self, boolValue):
        self.is_communicant = boolValue

    def addOutService(self, out_service):
        self.provided_services[out_service.name] = out_service

    def addInService(self, in_service):
        self.consumed_services[in_service.name] = in_service


class Link(Resource):
    def __init__(self, start_LRU, end_LRU):
        super().__init__(giveLinkName(start_LRU, end_LRU))
        self.start = start_LRU
        self.end = end_LRU
        self.is_communicant = True
        self.resource_type = 'LINK'
        serv = srv.CommunicationService()
        self.provided_services[serv.name] = serv