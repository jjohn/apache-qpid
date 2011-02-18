#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

__doc__ = """
            XML utilities used by spec.py
            
            Change History:
            -----------------
            
                Author      Date        Changes
                -------     ------      ---------
                Jimmy John  06/06/2007  Added doc strings for all functions
                                        Added __str__, __repr__, prettyPrint, prepareForPrettyPrint functions for the Node class
                                        Modified Node class to add a new member '_visited'
                Jimmy John  06/11/2007  Modified the prettyPrint function to return valid xml 
                Jimmy John  06/12/2007  Removed the __str__, __repr__ functions
                                        Modified createTag function to work even if attributes is None
            
          """
          
import xml.sax
from xml.sax.handler import ContentHandler

# ---------------
def parse(file):
  """
  interface to the outside world
  
  parses an xml spec file  and returns an object representation of it
  """
  doc = Node("root")
  xml.sax.parse(file, Builder(doc))
  return doc

# ----------
# ----------
class Node:
  """
  class representing each node of the input xml
  """

  # ------------------------------------------------------------------
  def __init__(self, name, attrs = None, text = None, parent = None):
    """
    initialises a Node object
    """
    self.name = name
    self.attrs = attrs
    self.text = text
    self.parent = parent
    self.children = []
    self._visited = False
    if parent != None:
      parent.children.append(self)

  # ----------------------------------------
  def get_bool(self, key, default = False):
    """
    returns the value of a node or an attribute of a node as a True/False value
    """
    v = self.get(key)
    if v == None:
      return default
    else:
      return bool(int(v))

  # ---------------
  def index(self):
    """
    returns the position of the node in the children list of it's parent
    """
    if self.parent:
      return self.parent.children.index(self)
    else:
      return 0

  # ------------------
  def has(self, key):
    """
    returns a True/False value if a node has 'key' as a name of a node or attribute
    """
    try:
      result = self[key]
      return True
    except KeyError:
      return False
    except IndexError:
      return False

  # ----------------------------------
  def get(self, key, default = None):
    """
    returns the value of the node or attribute specified by 'key'
    """
    if self.has(key):
      return self[key]
    else:
      return default

  # --------------------------
  def __getitem__(self, key):
    """
    called whenever an item is accessed through an object
    calls __getstr__ or __getint__ as appropriate
    """
    if callable(key):
      return filter(key, self.children)
    else:
      t = key.__class__
      meth = "__get%s__" % t.__name__
      if hasattr(self, meth):
        return getattr(self, meth)(key)
      else:
        raise KeyError(key)

  # --------------------------
  def __getstr__(self, name):
    """
    called by the __getitem__ function, when the argument to __getitem__ is a string
    i.e. this function returns the child node whose name is 'name'
    NOTE: attributes are accessed by prepending a '@' to it's name
    """
    if name[:1] == "@":
      return self.attrs[name[1:]]
    else:
      return self[lambda nd: nd.name == name]

  # ---------------------------
  def __getint__(self, index):
    """
    called by the __getitem__ function, when the argument to __getitem__ is an integer
    i.e. this function returns the child node indexed by 'index'
    """
    return self.children[index]

  # ------------------
  def __iter__(self):
    """
    function to make the Node class support the iteration protocol
    """
    return iter(self.children)

  # --------------
  def path(self):
    """
    retruns the path to the node, starting from the root e.g. /root/a/b/c
    """
    if self.parent == None:
      return "/%s" % self.name
    else:
      return "%s/%s" % (self.parent.path(), self.name)

  # ------------------------------------------      
  def prepareForPrettyPrint(self, index = 0):
    """
    marks all the nodes as NOT visited
    """
    self._visited = False
    if self.children:
       if index < len(self.children):
          self.children[index].prepareForPrettyPrint()
          index += 1
          self.prepareForPrettyPrint(index)

  # ----------------------------------------------------------
  def createTag(self, tagName, attrs, content, indent_level):
    """
    helpre function for prettyPrint
    """
    xml = ''
    
    xml += '\n' + indent_level*'\t' + '<%s ' % (tagName)
    
    #attrs can be None
    try:
        if self.attrs.getLength():
            for attr in attrs.keys():
                xml += attr + '=\"' + attrs[attr] + '\" '
    except AttributeError:
        pass
        
    xml += '>'
    
    #sometimes content can be None
    try:
        xml += content.strip()
    except AttributeError:
        pass
    
    return xml
    
  # --------------------------------------------------------
  def prettyPrint(self, indent_level=0, parsed_output=''):
    """
    prints out a tree representation of the contents of the Node
    """
    if indent_level == 0 and parsed_output == '':
        self.prepareForPrettyPrint()
        
        parsed_output = '<?xml version = "1.0"?>\n'
        parsed_output += self.createTag(self.name, self.attrs, self.text, indent_level)
        parsed_output += '\n'
      
    not_visited_children = filter(lambda node: node._visited == False, self.children)
    if not_visited_children:

        child_index = self.children.index(not_visited_children[0])
        self.children[child_index]._visited = True
        child = self.children[child_index]
        indent_level += 1
        
        parsed_output += self.createTag(child.name, child.attrs, child.text, indent_level)
        parsed_output = child.prettyPrint(indent_level, parsed_output)
        indent_level -=1
        parsed_output = self.prettyPrint(indent_level, parsed_output)
        return parsed_output
        
    else:
        if self.children:
           parsed_output += '\n' + indent_level*'\t' + '</%s>' % (self.name)
        else:
           parsed_output += '</%s>' % (self.name)
        
        return parsed_output
    
# -----------------------------
# -----------------------------
class Builder(ContentHandler):
  """
  ContentHandler class which handles the creation of the tree representation of the xml doc
  """

  # -------------------------------- 
  def __init__(self, start = None):
    """
    initialization...
    """
    self.node = start

  # ------------------------------------
  def __setitem__(self, element, type):
    """
    ?
    """
    self.types[element] = type

  # -----------------------------------
  def startElement(self, name, attrs):
    """
    called by the sax parser whenever start of an element is encountered
    creates a new Node object of the tag encountered
    """
    self.node = Node(name, attrs, None, self.node)

  # --------------------------
  def endElement(self, name):
    """
    called by the sax parser whenever end of an element is encountered
    """
    self.node = self.node.parent

  # -----------------------------
  def characters(self, content):
    """
    assigns the content of the xml tag to the Node object
    """
    if self.node.text == None:
      self.node.text = content
    else:
      self.node.text += content
      

