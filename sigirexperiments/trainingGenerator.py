import json

from ERtasks.models import Cora_labeled
from sigirexperiments import models,processhelper


def basicTrainingDataGenerator(username):
    print(username)
    traingdata = []
    testingdata = []
    validationdata = []
    dataset = Cora_labeled.objects.all()
    entitys = models.sigirCoraToAttrEntity.objects.filter(user=username)
    for record in dataset:
        syns = entitys.filter(cora_id=record.id)
        temp = syns.count()
        if temp > 2:
            print(temp)
            text = record.cleantext
            dict = {}
            texttemp = []
            for syn in syns:

                print(syn)
                synoym = syn.attrsynonym.synonym
                aa = processhelper.simpledatacleaning(synoym)
                aalist = aa.split(' ')
                for item in aalist:
                    dict[item] = syn.attrsynonym.value.attr.attrname
                # text = text.replace(synoym,' '+synoym+'###'+syn.attrsynonym.value.attr.attrname+' ')
            # text = processhelper.simpledatacleaning(text)
            textlist = text.split(' ')
            for item in textlist:
                if item in dict.keys():
                    texttemp.append(item+'/'+dict[item])
                else:
                    texttemp.append(item+'/NULL')
            if temp < 4:
                validationdata.append(' '.join(texttemp))
            else:
                traingdata.append(' '.join(texttemp))
        else:
            testingdata.append(record.cleantext)
    return traingdata,testingdata,validationdata


def basicTrainingDataDenseGenerator(username):
    print(username)
    traingdata = []
    testingdata = []
    validationdata = []
    dataset = Cora_labeled.objects.all()
    entitys = models.sigirCoraToAttrEntity.objects.filter(user=username)
    for record in dataset:
        syns = entitys.filter(cora_id=record.id)
        temp = syns.count()
        if temp > 2:
            print(temp)
            text = record.cleantext
            dict = {}
            texttemp = []
            for syn in syns:

                print(syn)
                synoym = syn.attrsynonym.synonym
                aa = processhelper.simpledatacleaning(synoym)
                aalist = aa.split(' ')
                for item in aalist:
                    dict[item] = syn.attrsynonym.value.attr.attrname
                # text = text.replace(synoym,' '+synoym+'###'+syn.attrsynonym.value.attr.attrname+' ')
            # text = processhelper.simpledatacleaning(text)
            textlist = text.split(' ')
            for item in textlist:
                if item in dict.keys():
                    texttemp.append(item+'/'+dict[item])
                else:
                    print('null')
            if temp < 4:
                validationdata.append(' '.join(texttemp))
            else:
                traingdata.append(' '.join(texttemp))
        else:
            testingdata.append(record.cleantext)
    return traingdata,testingdata,validationdata


def AttributeTrainingDataGenerator(username, attr_id):
    print(username)
    traingdata = []
    testingdata = []
    validationdata = []
    dataset = Cora_labeled.objects.all()
    entitys = models.sigirCoraToAttrEntity.objects.filter(user=username)
    for record in dataset:
        syns = entitys.filter(cora_id=record.id)

        if syns:
            attrids = [ syn.attrsynonym.value.attr_id for syn in syns]
            if attr_id in attrids:
                text = record.cleantext
                dict = {}
                texttemp = []
                for syn in syns:

                    print(syn)
                    synoym = syn.attrsynonym.synonym

                    aa = processhelper.simpledatacleaning(synoym)
                    aalist = aa.split(' ')
                    for item in aalist:
                        if syn.attrsynonym.value.attr_id == attr_id:
                            dict[item] = syn.attrsynonym.value_id
                        else:
                            dict[item] = 'ooo'
                    # text = text.replace(synoym,' '+synoym+'###'+syn.attrsynonym.value.attr.attrname+' ')
                # text = processhelper.simpledatacleaning(text)
                textlist = text.split(' ')
                for item in textlist:
                    if item in dict.keys():
                        texttemp.append(item + '/' + str(dict[item]))
                    else:
                        texttemp.append(item + '/NULL')
                traingdata.append(' '.join(texttemp))
            else:
                testingdata.append(record.cleantext)
        else:
            testingdata.append(record.cleantext)

    validationdata = traingdata
    return traingdata,testingdata,validationdata


def AttributeTrainingDataDenseGenerator(username, attr_id):
    print(username)
    traingdata = []
    testingdata = []
    validationdata = []
    dataset = Cora_labeled.objects.all()
    entitys = models.sigirCoraToAttrEntity.objects.filter(user=username)
    for record in dataset:
        syns = entitys.filter(cora_id=record.id)

        if syns:
            attrids = [ syn.attrsynonym.value.attr_id for syn in syns]
            if attr_id in attrids:
                text = record.cleantext
                dict = {}
                texttemp = []
                for syn in syns:

                    print(syn)
                    synoym = syn.attrsynonym.synonym

                    aa = processhelper.simpledatacleaning(synoym)
                    aalist = aa.split(' ')
                    for item in aalist:
                        if syn.attrsynonym.value.attr_id == attr_id:
                            dict[item] = syn.attrsynonym.value.value
                        else:
                            dict[item] = 'ooo'
                    # text = text.replace(synoym,' '+synoym+'###'+syn.attrsynonym.value.attr.attrname+' ')
                # text = processhelper.simpledatacleaning(text)
                textlist = text.split(' ')
                for item in textlist:
                    if item in dict.keys():
                        texttemp.append(item + '/' + dict[item])
                    else:
                        # texttemp.append(item + '/NULL')
                        print(item + '/NULL')
                traingdata.append(' '.join(texttemp))
            else:
                testingdata.append(record.cleantext)
        else:
            testingdata.append(record.cleantext)

    validationdata = traingdata
    return traingdata,testingdata,validationdata

def AttributeTrainingDataMixGenerator(username, attr_id):
    print(username)
    traingdata = []
    testingdata = []
    validationdata = []
    dataset = Cora_labeled.objects.all()
    entitys = models.sigirCoraToAttrEntity.objects.filter(user=username)
    for record in dataset:
        syns = entitys.filter(cora_id=record.id)

        if syns:
            attrids = [ syn.attrsynonym.value.attr_id for syn in syns]
            if attr_id in attrids:
                text = record.cleantext
                dict = {}
                texttemp = []
                for syn in syns:

                    print(syn)
                    synoym = syn.attrsynonym.synonym

                    aa = processhelper.simpledatacleaning(synoym)
                    aalist = aa.split(' ')
                    for item in aalist:
                        if syn.attrsynonym.value.attr_id == attr_id:
                            dict[item] = syn.attrsynonym.value_id
                        else:
                            dict[item] = 'ooo'
                    # text = text.replace(synoym,' '+synoym+'###'+syn.attrsynonym.value.attr.attrname+' ')
                # text = processhelper.simpledatacleaning(text)
                textlist = text.split(' ')
                left = list(set(textlist).difference(set(dict.keys())))
                for item in textlist:
                    if item in dict.keys():
                        texttemp.append(item + '/' + str(dict[item]))
                    else:
                        # texttemp.append(item + '/NULL')
                        print(item + '/NULL')
                for i in range(len(left)):
                    if i < 3:
                        texttemp.append(left[i] + '/NULL')
                traingdata.append(' '.join(texttemp))
            else:
                testingdata.append(record.cleantext)
        else:
            testingdata.append(record.cleantext)

    validationdata = traingdata
    return traingdata,testingdata,validationdata

def basicTrainingDataGenerator2(corahbf,dataset):
    traingdata = []
    ordered_layers_dict = corahbf.get_orderlayers_dict()
    for k,v in ordered_layers_dict.items():
        layer = corahbf.get_single_layer(v)
        print(layer.get_layerName(), " at layer:", layer.get_level())
        ordered_nodes_dict = layer.get_ordered_nodes_dict()
        layerName = layer.get_layerName()
        for order,value in ordered_nodes_dict.items():
            node = layer.get_single_child(value)
            print(" ", node.get_attributeValue(), ' at order:', node.get_node_order(), " size:", node.get_node_size(),
                  'indexed records:', node.get_index_recordids())
            node_edges = node.get_edges_dict()
            print(' ',json.dumps(node_edges))
            syns = node.get_children()
            for syn in syns.keys():
                print("     ", syn, ":", syns[syn])

