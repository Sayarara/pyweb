from collections import defaultdict
from  sigirexperiments import  models
from ERtasks.models import Cora_labeled
from DEXTRA import precluster
import json

class HBForest():
    # root 为数据集名称
    def __init__(self, hbfname):
        self.children_dict = {}
        self.hbfname = hbfname
        self.forest_dict = {}
        self.forest_dict[self.hbfname] = self.children_dict
        self.ordered_layers_dict = {}
        self.dataset_records_ids = []

    def set_dataset_records_ids(self,ids):
        self.dataset_records_ids = ids

    def get_dataset_records_ids(self):
        return self.dataset_records_ids

    # 获取数据集名称
    def get_hbfname(self):
        return self.hbfname

    #添加层级树
    def add_hbflayer(self, *args):
        #子节点中存储两个值，属性名称attr和对应的属性子树对象attrObj
        attr = args[0]
        value = args[1]
        syn = args[2]
        ids = args[3]
        #如果已经有某颗属性子树，则获取attrObj对象，添加新的value值
        if attr in self.children_dict.keys():
            layer = self.children_dict[attr]
            layer.add_valueNode(value, syn, ids)
        #否则创建一颗新的子树
        else:
            layer = HBFlayer(attr)
            layer.add_valueNode(value,syn,ids)
            self.children_dict[attr] = (layer)

    def get_all_layers(self):
        return self.children_dict

    def get_single_layer(self,attributeName):
        return self.children_dict[attributeName]

    def get_forest(self):
        return self.forest_dict

    def set_orderlayers_dict(self,dict):
        self.ordered_layers_dict = dict

    def get_orderlayers_dict(self):
        return self.ordered_layers_dict


class HBFlayer():
    #层级树，创建树是必须指定根结点，root为attribute name，each layer stands for a attribute
    #整颗森林存储在tree_dict中，key为root，value为children_dict
    #children_dict中存储所有的子节点
    def __init__(self, attributeName):
        self.tree_dict = {}
        self.children_dict = {}
        self.attributeName = attributeName
        self.tree_dict[self.attributeName] = self.children_dict
        self.level = 1
        self.ordered_nodes_dict = {}

    def set_ordered_nodes_dict(self,dict):
        self.ordered_nodes_dict = dict

    def get_ordered_nodes_dict(self):
        return self.ordered_nodes_dict

    #获取根结点的方法
    def get_layerName(self):
        return self.attributeName

    #添加子节点
    def add_valueNode(self, *args):
        #子节点中存储两个值，属性名称attr和对应的属性子树对象attrObj
        value = args[0]
        syn = args[1]
        ids = args[2]

        #如果已经有某个节点，则获取节点对象，添加新的syn值
        if value in self.children_dict.keys():
            valuenode = self.children_dict[value]
            valuenode.add_syn_child(syn, ids)
        #否则创建一颗新的节点
        else:
            valuenode = HBFlayerNode(value)
            valuenode.add_syn_child(syn,ids)
            self.children_dict[value] = (valuenode)

    #获取某个特定节点
    def get_single_child(self, value):
        return self.children_dict[value]

    #获取该层级树的所有子节点
    def get_all_children(self):
        return self.children_dict

    #获取整颗树
    def get_tree(self):
        return self.tree_dict

    def get_level(self):
        return self.level

    def set_level(self,level):
        self.level = level

#第二层，节点
class HBFlayerNode():
    #初始化方法，创建树时必须指定根结点，不允许创建空树，根结点的值为属性value
    #children_dict存储所有的子节点，子节点包括两个值，一个是该属性的某个值value，一个是该值对record的倒排索引
    #属性子树中的sum值，统计该子树一共获取了多少个值，方便之后根据该值计算每个值出现的频率
    def __init__(self, value):
        # root is attr, children are value-[record indexs] pairs
        self.value = value
        self.level = 1
        self.index_records = []
        self.children_dict = {}  # children are values in down level-[interaction record indexs] pairs
        self.parent_dict = {}  ## parent are values in up level-[interaction record indexs] pairs
        self.order = 0
        self.syns_dict = {} # {syn: [record ids]}
        self.size = 0
        self.edges_dict = {}

    def set_edges_dict(self,dict):
        self.edges_dict = dict

    def get_edges_dict(self):
        return self.edges_dict

    def get_edges_for_anode(self,level,nodename):
        layer_edges_dict =  self.edges_dict[level]
        if nodename in layer_edges_dict.keys():
            return layer_edges_dict[nodename]
        else:
            return None

    def get_edges_for_alayer(self,level):
        if level in self.edges_dict.keys():
            return self.edges_dict[level]
        else:
            return None


    # ids=[], 存记录的索引值
    def add_syn_child(self, syn, ids):
        self.index_records.extend(ids)
        self.index_records = list(set(self.index_records))
        self.size = len(self.index_records)
        if syn in self.syns_dict.keys():
            self.syns_dict[syn].extend(ids)
        else:
            self.syns_dict[syn] = ids
    #获取根结点
    def get_attributeValue(self):
        return self.value

    #获取全部子节点
    def get_children(self):
        return self.syns_dict



    def get_single_valueNode(self,value):
        return self.children_dict[value]

    def add_record_indexs(self, idx):
        self.index_records.extend(idx)



    def get_index_recordids(self):
        return self.index_records

    def get_node_order(self):
        return self.order

    def set_order(self,order):
        self.order = order
    def get_node_size(self):
        return  self.size

def hbf():
    return defaultdict(hbf)

def constructHBFfordataset(userid):
    ahbf = hbf()
    attras = models.sigirCoraAttr.objects.filter(userid=userid)
    for attra in attras:
        ahbf[attra.attrname]
        vals = models.sigirCoraAttrValue.objects.filter(attr_id=attra.id)
        for val in vals:
            ahbf[attra.attrname][val.value]
            syns = models.sigirCoraValueSynonym.objects.filter(value=val)
            for syn in syns:
                entitys = models.sigirCoraToAttrEntity.objects.filter(attrsynonym_id=syn.id)
                ahbf[attra.attrname][val.value][syn.synonym]=[entity.cora_id for entity in entitys]
                # ahbf[attra.attrname][val.value].extend([entity.cora_id for entity in entitys])
                #
                #                 # for entity in entitys:
                #                 #     ahbf[attra.attrname][val.value][syn.synonym][entity.cora_id]
    return  ahbf


def printHBF(ahbf):
    attributes = ahbf.keys()  # attribute names
    print(attributes)
    for attra in attributes:
        print(attra)
        values = ahbf[attra].keys()  # values for attribute attra
        for value in values:
            print(" ", value)
            syns = ahbf[attra][value].keys()
            for syn in syns:
                print("     ", syn, ":", ahbf[attra][value][syn])



def printOrderedHBF(corahbf):
    layers = corahbf.get_all_layers()
    for layername in layers.keys():
        layer = layers[layername]
        print(layer.get_layerName(), " at layer:", layer.get_level())
        nodes = layer.get_all_children()
        for nodeName in nodes.keys():
            node = nodes[nodeName]
            print(" ", node.get_attributeValue(),' at order:',node.get_node_order()," size:", node.get_node_size(),'indexed records:', node.get_index_recordids())
            syns = node.get_children()
            for syn in syns.keys():
                print("     ", syn, ":", syns[syn])

def printOrderedHBFByOrder(corahbf):
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    for k,v in ordered_layers_dict.items():
        layer = corahbf.get_single_layer(v)
        print(layer.get_layerName(), " at layer:", layer.get_level())
        ordered_nodes_dict = layer.get_ordered_nodes_dict()
        for order,value in ordered_nodes_dict.items():
            node = layer.get_single_child(value)
            print(" ", node.get_attributeValue(), ' at order:', node.get_node_order(), " size:", node.get_node_size(),
                  'indexed records:', node.get_index_recordids())
            node_edges = node.get_edges_dict()
            print(' ',json.dumps(node_edges))
            syns = node.get_children()
            for syn in syns.keys():
                print("     ", syn, ":", syns[syn])

def printOrderedHBFByOrderOnly(corahbf):
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    for k,v in ordered_layers_dict.items():
        layer = corahbf.get_single_layer(v)
        print(layer.get_layerName(), " at layer:", layer.get_level())
        ordered_nodes_dict = layer.get_ordered_nodes_dict()
        if k == 1:
            after_layer = k + 1
            for order, value in ordered_nodes_dict.items():
                node = layer.get_single_child(value)
                print(" ", node.get_attributeValue(), ' at order:', node.get_node_order(), " size:",
                      node.get_node_size(),
                      'indexed records:', node.get_index_recordids())
                node_edges_after_layer = node.get_edges_for_alayer(after_layer)
                print('     after_layer:', json.dumps(node_edges_after_layer))
                node_edges = node.get_edges_dict()
                print('     all_layer:', json.dumps(node_edges))
        else:
            if k == len(ordered_layers_dict):
                pre_layer = k - 1

                for order, value in ordered_nodes_dict.items():
                    node = layer.get_single_child(value)
                    print(" ", node.get_attributeValue(), ' at order:', node.get_node_order(), " size:",
                          node.get_node_size(),
                          'indexed records:', node.get_index_recordids())
                    # node_edges = node.get_edges_dict()
                    node_edges_pre_layer = node.get_edges_for_alayer(pre_layer)
                    print('     pre_layer', json.dumps(node_edges_pre_layer))
                    node_edges = node.get_edges_dict()
                    print('     all_layer:', json.dumps(node_edges))
            else:
                pre_layer = k-1
                after_layer = k+1
                for order, value in ordered_nodes_dict.items():
                    node = layer.get_single_child(value)
                    print(" ", node.get_attributeValue(), ' at order:', node.get_node_order(), " size:",
                          node.get_node_size(),
                          'indexed records:', node.get_index_recordids())
                    # node_edges = node.get_edges_dict()
                    node_edges_pre_layer = node.get_edges_for_alayer(k-1)
                    print('     pre_layer', json.dumps(node_edges_pre_layer))
                    node_edges_after_layer = node.get_edges_for_alayer(after_layer)
                    print('     after_layer:', json.dumps( node_edges_after_layer))
                    node_edges = node.get_edges_dict()
                    print('     all_layer:', json.dumps(node_edges))





def constructOrederedHBFFromDataset(userid,dataset):
    ahbf = constructHBFfordataset(userid=userid)
    orderhbf = constructOrderedHBF(ahbf=ahbf,dataset=dataset)
    record_ids = [ item.id for item in dataset]
    orderhbf.set_dataset_records_ids(record_ids)
    return orderhbf


def constructOrderedHBF(ahbf,dataset):
    record_ids = [item.id for item in dataset]

    attributes = ahbf.keys() # attribute names
    print(attributes)

    orderhbf = HBForest('cora')
    orderhbf.set_dataset_records_ids(record_ids)
    layer_order_dict = {}

    for attra in attributes:
        print(attra)
        values = ahbf[attra].keys() # values for attribute attra
        # print(values)
        attra_nodesize_dict = {}
        recordids_has_attra = []
        for value in values:
            print(" ",value)
            # print(" ",ahbf[attra][value])
            syns = ahbf[attra][value].keys()
            for syn in syns:
                print("     ",syn,":",ahbf[attra][value][syn])
                orderhbf.add_hbflayer(attra,value,syn,ahbf[attra][value][syn])
                recordids_has_attra.extend(ahbf[attra][value][syn])
            attra_nodesize_dict[value] = orderhbf.get_single_layer(attra).get_single_child(value). get_node_size()
        list_sort_value_desc = precluster.sort_dict(attra_nodesize_dict)
        order = 1
        # max = []
        ordered_nodes_dict = {}
        for item in list_sort_value_desc:
            orderhbf.get_single_layer(attra).get_single_child(item[0]).set_order(order)
            ordered_nodes_dict[order]=item[0]
            order = order+1
            # if len(max) == 0:
            #     max.append(value)
        ordered_nodes_dict[order] = 'NULL'
        orderhbf.add_hbflayer(attra,'NULL','NULL',list(set(record_ids).difference(set(recordids_has_attra))))
        orderhbf.get_single_layer(attra).set_ordered_nodes_dict(ordered_nodes_dict)
        layer_order_dict[attra] = list_sort_value_desc[0][1]
    layers = precluster.sort_dict(layer_order_dict)
    level = 1
    order_layers = {}
    for item in  layers:
        orderhbf.get_single_layer(item[0]).set_level(level)
        order_layers[level] = item[0]
        level = level + 1
    orderhbf.set_orderlayers_dict(order_layers)
    return orderhbf


def computeEdges(corahbf):
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    sortedkeys = sorted(ordered_layers_dict.keys())
    for i in range(len(sortedkeys)):
        edges_dict = {}
        currentlayerkey = sortedkeys[i]
        layer = corahbf.get_single_layer(ordered_layers_dict[currentlayerkey])
        ordered_nodes_dict = layer.get_ordered_nodes_dict()
        for order, value in ordered_nodes_dict.items():
            node = layer.get_single_child(value)
            node_edges_dict = {}
            node_index_records = node.get_index_recordids()
            for j in range(len(sortedkeys)):

                if i != j:
                    # estimate each layer edges
                    focusedlayerkey = sortedkeys[j]
                    focusedlayer = corahbf.get_single_layer(ordered_layers_dict[focusedlayerkey])
                    focused_nodes_dict  = focusedlayer.get_ordered_nodes_dict()
                    focused_level_edges_dict = {}
                    for forder,fvalue in focused_nodes_dict.items():
                        focused_node = focusedlayer.get_single_child(fvalue)
                        inter = list(set(node_index_records).intersection(set(focused_node.get_index_recordids())))
                        if len(inter) > 0:
                            focused_level_edges_dict[fvalue] = inter
                    node_edges_dict[focusedlayerkey] = focused_level_edges_dict
            node.set_edges_dict(node_edges_dict)
    return corahbf


def estimateN_ACR(corahbf):
    dict = {}
    total_records = corahbf.get_dataset_records_ids()
    layers = corahbf.get_all_layers()
    for id in total_records:
        count = 0
        for layername in layers.keys():
            layer = layers[layername]
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()
            if id not in nullNodeRecords:
                count = count + 1
        dict[id] = count

    count_dict = {}
    for k,v in dict.items():
        if v in count_dict.keys():
            count_dict[v] = count_dict[v]+1
        else:
            count_dict[v] = 1

    for k,v in count_dict.items():
        print(k, v)
        # print(k,v/len(total_records))
    sum_count_dict = {}
    if 0 in sum_count_dict.keys():
        sum_count_dict[0] = count_dict[0]
    for i in range(1,len(count_dict)):
        sum_count_dict[i]= 0
        for j  in range(i,len(count_dict)):
            sum_count_dict[i] = sum_count_dict[i]+count_dict[j]
    for k,v in sum_count_dict.items():
        print(k, v / len(total_records))
        sum_count_dict[k] = v / len(total_records)
    return sum_count_dict


def collectSubrecords0(dataset,ids,username):
    datas = dataset.filter(id__in = ids)
    # 找records的最大公共 values
    cora2entity = models.sigirCoraToAttrEntity.objects.filter(user=username,cora_id__in=ids).order_by('cora_id')

from sigirexperiments import  processhelper,dextrapreclustering
def collectSubrecords(node,dataset,username):
    # dataset = Cora_labeled.objects.all()
    nodeRecords = node.get_index_recordids()
    edges_dict = node.get_edges_dict()
    # find max common values
    commonValues = []
    for layer in edges_dict.keys():
        layer_edges_dict = edges_dict[layer]
        for nodevalue in layer_edges_dict.keys():
            recordsids = layer_edges_dict[nodevalue]
            if set(nodeRecords).issubset(set(recordsids)):
                commonValues.append(nodevalue)
    print(node.get_attributeValue(),':',nodeRecords)
    commonValues.append(node.get_attributeValue())
    # print(commonValues)
    datas = dataset.filter(id__in=nodeRecords)
    # record_id_dict = {}
    # for i in range(len(nodeRecords)):
    #     record_id_dict[i] = nodeRecords[i]
    # collect subrecords
    subrecords = []
    for data in datas:
        # print(data.cleantext)
        subrecord = data.cleantext
        coraent = models.sigirCoraToAttrEntity.objects.filter(user=username,cora_id=data.id)
        for cc in coraent:
            syn = cc.attrsynonym.synonym
            cleansyn = processhelper.simpledatacleaning(syn)
            if cc.attrsynonym.value.value in commonValues:
                # print(cleansyn)
                subrecord = subrecord.replace(cleansyn,'')
                # print(subrecord)
            else:
                subrecord = subrecord.replace(cleansyn,cc.attrsynonym.value.value)
        subrecords.append(subrecord)
    return subrecords


import affinegap
def hbfClusterView(corahbf,dataset,acr_threshold,username,dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict,0,-1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:',nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                # split
                nodeRecords = node.get_index_recordids()
                if len(nodeRecords) > 1:
                    subrecords = collectSubrecords(node=node,dataset=dataset,username=username)
                    subgroups = dextrapreclustering.affinegaphClustering(data=subrecords)
                else:
                    subgroups = [1]
                for i in range(len(subgroups)):
                    cluster_dict[nodeRecords[i]] = subgroups[i]+count
                count = count+len(subgroups)

            # merge
            if nullNodeRecords:
                removej = []
                notnullrecords = [k for k in cluster_dict.keys()]
                for j in range(len(nullNodeRecords)):
                    tempmin = [100000000, 0]
                    # for i in range(len(cluster_dict)):
                    #     data = dataset.filter(id__in=[nodeRecords[i], nullNodeRecords[j]])
                    for i in notnullrecords:
                        data = dataset.filter(id__in=[i, nullNodeRecords[j]])
                        d3 = affinegap.normalizedAffineGapDistance(data[0].cleantext, data[1].cleantext)
                        if d3 < tempmin[0]:
                            tempmin[0] = d3
                            tempmin[1] = i
                    if tempmin[0] < dis_threshold:
                        cluster_dict[nullNodeRecords[j]] = cluster_dict[i]
                        removej.append(nullNodeRecords[j])
                remaing = list(set(nullNodeRecords).difference(set(removej)))
                count = count+1
                for id in remaing:
                    cluster_dict[id] = count
                    count = count =1
    return cluster_dict

def hbfClusterViewSimple(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                # Simple leaf node
                nodeRecords = node.get_index_recordids()
                for i in range(len(nodeRecords)):
                    cluster_dict[nodeRecords[i]] = count
                count = count + len(nodeRecords)

            # merge
            if nullNodeRecords:
                count = count + 1

                for id in nullNodeRecords:
                    cluster_dict[id] = count
                    count = count +1
            print('cluster size:')
            return cluster_dict




def hbfClusterViewSimpleleavePath(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                # Simple leaf node
                nodeRecords = node.get_index_recordids()
                edges_dict = node.get_edges_dict()
                # find max common values
                commonValues = []
                for layer in edges_dict.keys():
                    layer_edges_dict = edges_dict[layer]
                    for nodevalue in layer_edges_dict.keys():
                        recordsids = layer_edges_dict[nodevalue]

                print(node.get_attributeValue(), ':', nodeRecords)
                commonValues.append(node.get_attributeValue())
                for i in range(len(nodeRecords)):
                    cluster_dict[nodeRecords[i]] = count
                count = count + len(nodeRecords)

            # merge
            if nullNodeRecords:
                count = count + 1

                for id in nullNodeRecords:
                    cluster_dict[id] = count
                    count = count +1
        print('cluster size:' )
        return cluster_dict


def hbfClusterViewSimple2(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                # Simple leaf node
                nodeRecords = node.get_index_recordids()
                if len(nodeRecords) > 10:
                    subrecords = collectSubrecords(node=node,dataset=dataset,username=username)
                    subgroups = dextrapreclustering.affinegaphClustering(data=subrecords)
                else:
                    subgroups = [1 for k in nodeRecords]
                for i in range(len(subgroups)):
                    cluster_dict[nodeRecords[i]] = subgroups[i]+count
                count = count+len(subgroups)

            # merge
            if nullNodeRecords:
                count = count + 1

                for id in nullNodeRecords:
                    cluster_dict[id] = count
                    count = count +1
            print('cluster size:')
            return cluster_dict

def hbfClusterViewSimple3(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                # Simple leaf node
                nodeRecords = node.get_index_recordids()
                if len(nodeRecords) > 20:
                    subrecords = collectSubrecords(node=node,dataset=dataset,username=username)
                    subgroups = dextrapreclustering.affinegaphClustering(data=subrecords)
                else:
                    subgroups = [1 for k in nodeRecords]
                for i in range(len(subgroups)):
                    cluster_dict[nodeRecords[i]] = subgroups[i]+count
                count = count+len(subgroups)

            # merge
            if nullNodeRecords:
                count = count + 1

                for id in nullNodeRecords:
                    cluster_dict[id] = count
                    count = count +1
            print('cluster size:')
            return cluster_dict


from  DEXTRA import precluster
def hbfClusterViewSimpleMinhash(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                #
                print('start spliting')
                nodeRecords = node.get_index_recordids()
                if len(nodeRecords) > 20:
                    print('start collect subrecords')
                    subrecords = collectSubrecordsSimple(node=node,dataset=dataset,username=username)
                    print('start hclustering')
                    clustdict = dextrapreclustering.affinegapSimpleClustering(data=subrecords)
                    cluster_membership = {}
                    for k, v in clustdict.items():
                        for d in v:
                            cluster_membership[d] = k
                    subgroups = [cluster_membership[i] for i in range(len(nodeRecords))]
                else:
                    subgroups = [1 for k in nodeRecords]
                for i in range(len(subgroups)):
                    cluster_dict[nodeRecords[i]] = subgroups[i]+count
                count = count+len(subgroups)
            # merge
            print('start merging-------')
            if nullNodeRecords:
                count = count + 1
                notnullrecords = [k for k in cluster_dict.keys()]
                notnulls = dataset.filter(id__in=notnullrecords)
                data1 = [item.cleantext for item in notnulls]
                notnullminhashs = processhelper.getMinHashs(data=data1)
                forest = processhelper.getMinhashforest2(minhashs=notnullminhashs)
                nulls = dataset.filter(id__in=nullNodeRecords)
                data2 = [item.cleantext for item in nulls]
                nullsminhashs = processhelper.getMinHashs(data=data2)
                for j in range(len(nullNodeRecords)):
                    # Using m1 as the query, retrieve top 1 keys that have the higest Jaccard
                    result = forest.query(nullsminhashs[j], 1)
                    for notnullkey in result:
                        jd = nullsminhashs[j].jaccard(notnullminhashs[notnullkey])
                        if jd > 0.3 and jd < 0.44:
                            print(j, ' maximum jaccard:', jd)
                            print('     ', data2[j])
                            print('     ', data1[notnullkey])
                        if jd > 0.38:
                            reid = notnullrecords[notnullkey]
                            cluster_dict[nullNodeRecords[j]] = cluster_dict[reid]
                        else:
                            cluster_dict[nullNodeRecords[j]] = count
                            count = count + 1
                print('cluster size:')
                return cluster_dict

def hbfClusterViewSimpleMinhashaffinegap(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                #
                print('start spliting')
                nodeRecords = node.get_index_recordids()
                if len(nodeRecords) > 20:
                    print('start collect subrecords')
                    subrecords = collectSubrecordsSimple(node=node,dataset=dataset,username=username)
                    print('start hclustering')
                    clustdict = dextrapreclustering.affinegapSimpleClustering(data=subrecords)
                    cluster_membership = {}
                    for k, v in clustdict.items():
                        for d in v:
                            cluster_membership[d] = k
                    subgroups = [cluster_membership[i] for i in range(len(nodeRecords))]
                else:
                    subgroups = [1 for k in nodeRecords]
                for i in range(len(subgroups)):
                    cluster_dict[nodeRecords[i]] = subgroups[i]+count
                count = count+len(subgroups)
            # merge
            print('start merging-------')
            if nullNodeRecords:
                count = count + 1
                notnullrecords = [k for k in cluster_dict.keys()]
                notnulls = dataset.filter(id__in=notnullrecords)
                data1 = [item.cleantext for item in notnulls]
                notnullminhashs = processhelper.getMinHashs(data=data1)
                forest = processhelper.getMinhashforest2(minhashs=notnullminhashs)
                nulls = dataset.filter(id__in=nullNodeRecords)
                data2 = [item.cleantext for item in nulls]
                nullsminhashs = processhelper.getMinHashs(data=data2)
                for j in range(len(nullNodeRecords)):
                    # Using m1 as the query, retrieve top 1 keys that have the higest Jaccard
                    result = forest.query(nullsminhashs[j], 1)
                    for notnullkey in result:
                        jd = nullsminhashs[j].jaccard(notnullminhashs[notnullkey])
                        d3 = affinegap.normalizedAffineGapDistance(data2[j], data1[notnullkey])
                        if jd > 0.3 and jd < 0.5:


                            print(j, ' maximum jaccard:', jd,' afgap:',d3)
                            print('     ', data2[j])
                            print('     ', data1[notnullkey])
                        if d3 < 3:
                            reid = notnullrecords[notnullkey]
                            cluster_dict[nullNodeRecords[j]] = cluster_dict[reid]
                        else:
                            cluster_dict[nullNodeRecords[j]] = count
                            count = count + 1
                print('cluster size:')
                return cluster_dict



def hbfClusterViewComplexMinhashaffinegap(corahbf, dataset, acr_threshold, username, dis_threshold):
    cluster_dict = {}
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    print(json.dumps(ordered_layers_dict))
    lendict = len(ordered_layers_dict)
    total_records = corahbf.get_dataset_records_ids()
    for k in range(lendict, 0, -1):
        layer = corahbf.get_single_layer(ordered_layers_dict[k])
        print(layer.get_layerName(), " at layer:", layer.get_level())
        # check the layer-ACR
        all_children_dict = layer.get_all_children()
        if 'NULL' in all_children_dict.keys():
            nullNode = layer.get_single_child('NULL')
            nullNodeRecords = nullNode.get_index_recordids()

            print('nullNodeRecords:', nullNodeRecords)
            layer_ACR = 1 - len(nullNodeRecords) / len(total_records)
        else:
            layer_ACR = 1
        # skip
        if layer_ACR < acr_threshold:
            continue
        else:
            count = 0
            ordered_nodes_dict = layer.get_ordered_nodes_dict()
            for order, value in ordered_nodes_dict.items():
                if value == 'NULL':
                    continue
                node = layer.get_single_child(value)
                #
                print('start spliting')
                nodeRecords = node.get_index_recordids()
                if len(nodeRecords) > 20:
                    print('start collect subrecords')
                    subrecords = collectSubrecordsSimple(node=node,dataset=dataset,username=username)
                    print('start hclustering')
                    clustdict = dextrapreclustering.affinegapSimpleClustering(data=subrecords)
                    cluster_membership = {}
                    for k, v in clustdict.items():
                        for d in v:
                            cluster_membership[d] = k
                    subgroups = [cluster_membership[i] for i in range(len(nodeRecords))]
                else:
                    subgroups = [1 for k in nodeRecords]
                for i in range(len(subgroups)):
                    cluster_dict[nodeRecords[i]] = subgroups[i]+count
                count = count+len(subgroups)
            # merge
            print('start merging-------')
            if nullNodeRecords:

                notnullrecords = [k for k in cluster_dict.keys()]
                notnulls = dataset.filter(id__in=notnullrecords)
                data1 = [item.cleantext for item in notnulls]
                notnullminhashs = processhelper.getMinHashs(data=data1)
                forest = processhelper.getMinhashforest2(minhashs=notnullminhashs)
                nulls = dataset.filter(id__in=nullNodeRecords)
                data2 = [item.cleantext for item in nulls]
                nullsminhashs = processhelper.getMinHashs(data=data2)
                for j in range(len(nullNodeRecords)):
                    # Using m1 as the query, retrieve top 1 keys that have the higest Jaccard
                    result = forest.query(nullsminhashs[j], 5)
                    tempp = [1000000,0]
                    count = count + 1
                    for notnullkey in result:
                        # jd = nullsminhashs[j].jaccard(notnullminhashs[notnullkey])
                        d3 = affinegap.normalizedAffineGapDistance(data2[j], data1[notnullkey])
                        if d3 < tempp[0]:
                            tempp[0] = d3
                            tempp[1] = notnullkey

                    if tempp[0] < 3:
                        reid = notnullrecords[tempp[1]]
                        cluster_dict[nullNodeRecords[j]] = cluster_dict[reid]
                    else:
                        cluster_dict[nullNodeRecords[j]] = count
                        count = count + 1
                print('cluster size:')
                return cluster_dict


def hbfaffinegapOnlyclusterSimple(corahbf, dataset, acr_threshold, username, dis_threshold):
    subrecords = []
    dataset = dataset.order_by('id')
    record_ids = [ data.id for data in dataset]
    for data in dataset:
        # print(data.cleantext)
        subrecord = data.cleantext
        coraent = models.sigirCoraToAttrEntity.objects.filter(user=username, cora_id=data.id)
        for cc in coraent:
            syn = cc.attrsynonym.synonym
            cleansyn = processhelper.simpledatacleaning(syn)
            subrecord = subrecord.replace(cleansyn, cc.attrsynonym.value.value)
        subrecords.append(subrecord)
    subgroups = dextrapreclustering.affinegaphClustering(data=subrecords)
    cluster_dict = {}
    for i in range(len(subgroups)):
        cluster_dict[record_ids[i]] = subgroups[i]
    return cluster_dict





def collectSubrecordsSimple(node,dataset,username):
    nodeRecords = node.get_index_recordids()
    datas = dataset.filter(id__in=nodeRecords)
    subrecords = [data.cleantext for data in datas]
    return subrecords













