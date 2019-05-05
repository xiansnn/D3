'''
Created on 10 sept. 2017

@author: chris
'''


from modelizer import resource_module as res

service_dict = {}

# definition of Service Domains
service_domain_dict = {}

# regles de nommage des servives


def giveALIVEserviceName(monitoring_host, monitored_neighbor):
    return monitoring_host.name + '_' + monitored_neighbor.name + '.ALIVE'


def giveMIDserviceName(provider):
    return 'MID.' + provider.name


def giveLINKserviceName(reporting_host, monitored_neighbor):
    return 'MID.'+reporting_host.name+'.'+monitored_neighbor.name+'.LINK'


class ServiceDomain():
    def __init__(self, name, QoS):
        self.name = name
        # quality of service from from better to worse
        self.QoS = QoS
        # on enregistre le nouveau domaine dans service_domain_dict
        service_domain_dict[self.name] = self
        # create declaration pattern
        self. declaration = self.name+' = '
        s0 = '{'
        for value in self.QoS:
            s0 += value+'>'
        self. declaration += s0[:-1]+'};'

    def __repr__(self):
        return 'DOM<'+self.name+'>'


class Service():
    '''
    classdocs
    '''

    def __init__(self, model, name, domain, provider, consumer):
        '''
        Constructor
        '''
        self.name = name
        self.domain = domain
        self.provider = provider
        self.consumer = consumer
        self.dependence = ''
        self.path_pattern = ''
        # creation declaration
        self.declaration = '\t\t' + self.name + '{'+self.domain.name + '},\n'

        # on enregistre le nouveau service dans service_dict
        service_dict.update({self.name: self})

        # on enregistre le nouveau service dans ses ressources source et cible
        if consumer != None:
            self.consumer.addInService(self)
        if provider != None:
            self.provider.addOutService(self)

        if (provider != None) & (consumer != None):
            self.path = model.getshortestPathWithLink(provider, consumer)
            if len(self.path) < 2:
                pass

            elif len(self.path) == 3:
                source_LRU_name = self.path[0].name
                link_name = self.path[1].name
                target_LRU_name = self.path[2].name
                s = source_LRU_name + ':' + self.name + ' -> ' + link_name + \
                    ':Communication -> ' + target_LRU_name+':' + self.name + ';\n'
                self.path_pattern += s

            elif len(self.path) > 3:
                source_LRU_name = self.path[0].name
                target_LRU_name = self.path[-1].name
                s0 = source_LRU_name+':'+self.name+' -> '
                for step in self.path[1:-1]:
                    s0 += step.name + ':Communication, '
                    t = step.resource_type
                    if t == 'LRU':
                        step.addOutService(CommunicationService())
                        step.is_communicant = True
                p = s0[0:-2]
                p += ' -> '+target_LRU_name+':'+self.name+';\n'
                self.path_pattern += p

    def __repr__(self):
        return 'SRV<'+self.name+'>'


class CommunicationService(Service):
    def __init__(self):
        domain = ServiceDomain('okko', ['OK', 'KO'])
        super().__init__(None, 'Communication', domain, None, None)
        # creation du pattern dependence
        s0 = ''
        s0 += '\tSERVICE ' + self.name + ' DEPENDS_ON status:\n'
        s0 += '\t\tOK IF status=OK,\n'
        s0 += '\t\tKO OTHERWISE;\n'
        self.dependence = s0


class LINKserviceGenerator():
    def __init__(self, model, maintenance_server_name):
        net = model.directed_net
        CMA = res.resource_dict[maintenance_server_name]
# netlist = list(filter(lambda x : x!= maintenance_server_name, net.node.keys()))
        for node in net:
            if node != maintenance_server_name:
                monitoring_host = res.resource_dict[node]
                for monitored_ALIVE_service in monitoring_host.ALIVE_service.values():
                    LINKservice(model, monitoring_host,
                                CMA, monitored_ALIVE_service)


class LINKservice(Service):
    def __init__(self, model, monitoring_host, consumer, monitored_ALIVE_service):
        m = monitored_ALIVE_service.provider
        name = giveLINKserviceName(monitoring_host, m)
        domain = ServiceDomain('LINK_state', ['UP', 'DEAD', 'not_refreshed'])
        super().__init__(model, name, domain, monitoring_host, consumer)
        # creation du pattern dependence
        s0 = ''
        s0 += '\tSERVICE ' + self.name + ' DEPENDS_ON ' + \
            monitored_ALIVE_service.name + ', status:\n'
        s0 += '\t\tDEAD IF ' + monitored_ALIVE_service.name + '=false & status=OK,\n'
        s0 += '\t\tnot_refreshed IF status=KO,\n'
        s0 += '\t\tUP OTHERWISE;\n'
        self.dependence = s0


class MIDserviceGenerator():
    def __init__(self, model, maintenance_server_name):
        net = model.directed_net
        CMA = res.resource_dict[maintenance_server_name]
        for node in net.nodes():
            if node != maintenance_server_name:
                lru = res.resource_dict[node]
                MIDservice(model, lru, CMA)


class MIDservice(Service):
    def __init__(self, model, provider, consumer):
        name = giveMIDserviceName(provider)
        domain = ServiceDomain('MID_state', ['OK', 'not_refreshed'])
        super().__init__(model, name, domain, provider, consumer)
        # creation du pattern dependence
        s0 = ''
        s0 += '\tSERVICE ' + self.name + ' DEPENDS_ON status:\n'
        s0 += '\t\tnot_refreshed IF status=KO,\n'
        s0 += '\t\tOK OTHERWISE;\n'
        self.dependence = s0


class ALIVEserviceGenerator():
    def __init__(self, model, all_neighbor=False):
        if all_neighbor == True:
            net = model.undirected_net
        else:
            net = model.directed_net
        # for node in net.adjacency_iter():
        for node in net.adjacency():
            host_name = node[0]
            monitoring_host = res.resource_dict[host_name]
            neighbor_dict = node[1]
            for neighbor in neighbor_dict:
                monitored_neighbor = res.resource_dict[neighbor]
                ALIVEservice(model, monitored_neighbor, monitoring_host)


class ALIVEservice(Service):
    def __init__(self, model, monitored_neighbor, monitoring_host):
        name = giveALIVEserviceName(monitoring_host, monitored_neighbor)
        domain = ServiceDomain('bool', ['true', 'false'])
        super().__init__(model, name, domain,
                         monitored_neighbor, monitoring_host)
        monitoring_host.ALIVE_service[self.name] = self
        s0 = ''
        s0 += '\tSERVICE ' + self.name + ' DEPENDS_ON status:\n'
        s0 += '\t\ttrue IF status=OK,\n'
        s0 += '\t\tfalse OTHERWISE;\n'
        self.dependence = s0
