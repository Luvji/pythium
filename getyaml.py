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

        for page, page_actions in yamldata[pages].items():
            if page == 'events':
                if isinstance(page_actions,(list)):
                    for eachtuple in page_actions:
                        serialiser.append(eachtuple[0])
                        serialisertarget.append(eachtuple[1])
                        serialiseractivity.append(yamldata[pages]['activity'])
                elif isinstance(page_actions,(dict)):
                    for k,v in page_actions.items():
                        serialiser.append(k)
                        serialisertarget.append(v)
                        serialiseractivity.append(yamldata[pages]['activity'])
                else:
                    print("\n\n?????????????????????\n\n this is something else\n")
    return  serialiser,serialisertarget,serialiseractivity


# print(yamldata[0]['login'])