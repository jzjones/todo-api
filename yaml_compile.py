import yaml
import os
import sys

merge_template = sys.argv[1]

class Loader(yaml.SafeLoader):

    def __init__(self, stream):

        self._root = os.path.split(stream.name)[0]

        super(Loader, self).__init__(stream)

    def include(self, node):

        print('include', node)
        print('scalar', self.construct_scalar(node))
        filename = os.path.join(self._root, self.construct_scalar(node))

        with open(filename, 'r') as f:
            data = yaml.load(f, Loader)
            print(data)
            return data

Loader.add_constructor('!include', Loader.include)

def expand_function(self, node):
  print(node)
  output = {'Fn::' + node.tag[1:]: node.value}
  # output = '\n' + 'Fn::' + node.tag[1:] + ': ' + node.value
  print(output)
  return output

Loader.add_constructor('!Sub', expand_function)
Loader.add_constructor('!GetAtt', expand_function)
Loader.add_constructor('!Ref', expand_function)
Loader.add_constructor('!Join', expand_function)

# for filename in os.listdir('templates/'):
#   if filename.endswith(".yaml"): 
#     print(filename)
#         # print(os.path.join(directory, filename))
#     continue
#   else:
#     continue

with open('template.yaml', 'r') as f:
  data = yaml.load(f, Loader)
  stream = file(merge_template, 'w')
  yaml.safe_dump(data, stream) 

    # yaml.dump(data, outfile, default_flow_style=False)
  print(data)