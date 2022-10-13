import sys

from ruamel.yaml import YAML
from ruamel.yaml.constructor import SafeConstructor
# from config import yml
from pathlib import Path  # or: from ruamel.std.pathlib import Path


def getyaml(yamlpath):
    def construct_yaml_map(self, node):
        # test if there are duplicate node keys
        data = []
        yield data
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            val = self.construct_object(value_node, deep=True)
            data.append((key, val))
    
    def construct_yaml_map_dict(self, node):
    # test if there are duplicate node keys
        keys = set()
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            if key in keys:
                break
            keys.add(key)
        else:
            data = {}  # type: Dict[Any, Any]
            yield data
            value = self.construct_mapping(node)
            data.update(value)
            return
        data = []
        yield data
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            val = self.construct_object(value_node, deep=True)
            data.append((key, val))

# construct_yaml_map_dict
    SafeConstructor.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map_dict)
    # SafeConstructor.add_constructor(u'tag:yaml.org,2002:map', construct_yaml_map)
    # yaml = YAML(typ='safe')
    # data = yaml.load(yaml_str)
    yaml = YAML(typ='safe')
    data = yaml.load(Path(yamlpath))
    return data
def serialise_data(yamlpath):
    (r'C:\Users\Administrator\Desktop\pyppium\sitemap.yaml') if yamlpath is None else yamlpath
    print("getting the yaml data from ",yamlpath)
    yamldata = getyaml(yamlpath)
    # print(type(yamldata))
    # print(yamldata)
    serialiser = []
    serialisertarget = []
    serialiseractivity = []
    for pages in yamldata:
        # print ("pages :::::::::",pages)
        # print ("type of pages :::::::::",type(pages))
        # print("\tyamldata[pages]",yamldata[pages])
        for page, page_actions in yamldata[pages].items():
            if page == 'events':
            
                # print ("\t\tpage :::::::::",page)
                # print ("\t\tyamldata[pages][page] :::::::::",yamldata[pages][page])
                # print ("\t\tpage_actions :::::::::",page_actions)
                # print("\ttype of pageaction:::::::::::",type(page_actions))
                # for x in page_actions:
                # print("\txxxxxxx",x)
                # print(">>>>>>>>>",type(page_actions))
                if isinstance(page_actions,(list)):
                    # print("\n\n\nthis is list",page_actions)
                    # print("typeof page_actions[0]0",type(page_actions[0]))
                    for eachtuple in page_actions:
                        # print("this is eachtuple",eachtuple)
                        # print("eachtuple[0]:::::::::",eachtuple[0])
                        serialiser.append(eachtuple[0])
                        serialisertarget.append(eachtuple[1])
                        serialiseractivity.append(yamldata[pages]['activity'])
                elif isinstance(page_actions,(dict)):
                    # print("\n\n\nthis is dict",page_actions)
                    for k,v in page_actions.items():
                        # print("kkkkkkkkkkkkkkkkkkkkkk",k)
                        # print("vvvvvvvvvvvvvvvvvvvvvv",v)
                        serialiser.append(k)
                        serialisertarget.append(v)
                        serialiseractivity.append(yamldata[pages]['activity'])
                        
                        # print("page_actions[v]",page_actions[v])
                else:
                    print("\n\n?????????????????????\n\n this is something else\n")
    # print(serialiser)
    # print(serialisertarget)
    return  serialiser,serialisertarget,serialiseractivity


# print(yamldata[0]['login'])