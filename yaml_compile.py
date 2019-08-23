import yaml
import os
import sys

merge_template = sys.argv[1]

class Loader(yaml.SafeLoader):

  def __init__(self, stream):

    self._root = os.path.split(stream.name)[0]

    super(Loader, self).__init__(stream)

  def include(self, node):

    filename = os.path.join(self._root, self.construct_scalar(node))

    with open(filename, 'r') as f:
      data = yaml.load(f, Loader)
      return data

  def expand_function(self, node):
    output = {'Fn::' + node.tag[1:]: node.value}
    return output
  
  def expand_helper(self, node):
    output = {node.tag[1:]: node.value}
    return output

  def function_path(self, node):
    output = "./dist/" + node.value
    return output

Loader.add_constructor('!include', Loader.include)
Loader.add_constructor('!Sub', Loader.expand_function)
Loader.add_constructor('!GetAtt', Loader.expand_function)
Loader.add_constructor('!Ref', Loader.expand_helper)
Loader.add_constructor('!Join', Loader.expand_function)
Loader.add_constructor('!function', Loader.function_path)

with open('template.yaml', 'r') as f:
  data = yaml.load(f, Loader)
  stream = file(merge_template, 'w')
  yaml.safe_dump(data, stream)
