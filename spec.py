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
            This module loads protocol metadata into python objects. It provides
            access to spec metadata via a python object model, and can also
            dynamically creating python methods, classes, and modules based on the
            spec metadata. All the generated methods have proper signatures and
            doc strings based on the spec metadata so the python help system can
            be used to browse the spec documentation. The generated methods all
            dispatch to the self.invoke(meth, args) callback of the containing
            class so that the generated code can be reused in a variety of
            situations.

            Change History:
            ###############

               Author     Date        Changes
               -------    ----------  --------
               Jimmy J    06/17/2007  Added doc strings for all functions
                                      Modified function Method.define_method so that __doc__ will return the contents of docstring()
          """

import re, textwrap, new, xmlutil

# -------------------
# -------------------
class SpecContainer:
  """
  Class encapsulating each of the accessable entities in the spec file e.g
  fields, constants, classes etc
  """

  # ------------------
  def __init__(self):
    """
    initializations...
    """
    self.items = []
    self.byname = {}
    self.byid = {}
    self.indexes = {}

  # -------------------
  def add(self, item):
    """
    adds the 'item' into data structures so they can be accessed later
    """
    if self.byname.has_key(item.name):
      raise ValueError("duplicate name: %s" % item)
    if self.byid.has_key(item.id):
      raise ValueError("duplicate id: %s" % item)
    self.indexes[item] = len(self.items)
    self.items.append(item)
    self.byname[item.name] = item
    self.byid[item.id] = item

  # ---------------------
  def index(self, item):
    """
    returns the index of the 'item' within this particular SpecContainer.
    typicall used by the Method class, to indicate the position of the field in the argument list e.g.
    method.fields.index(f)
    """
    try:
      return self.indexes[item]
    except KeyError:
      raise ValueError(item)

  # ------------------
  def __iter__(self):
    """
    function to support the iteration protocol
    """
    return iter(self.items)

  # -----------------
  def __len__(self):
    """
    function to return the number of items contained in this SpecContainer instance.
    this information can tell us the position of an argument in an field list
    """
    return len(self.items)

# --------------
# --------------
class Metadata:
  """
  Base class containing several common functions
  """

  PRINT = []

  # -------------------
  def __init__(self):
    """
    do-nothing function
    """
    pass

  # -----------------
  def __str__(self):
    """
    pretty prints contents of the object
    """
    args = map(lambda f: "%s=%s" % (f, getattr(self, f)), self.PRINT)
    return "%s(%s)" % (self.__class__.__name__, ", ".join(args))

  # ------------------
  def __repr__(self):
    """
    same as the __str__ function
    """
    return str(self)

# --------------------
# --------------------
class Spec(Metadata):
  """
  class encapsulating the object representation of the parsed xml specification document
  """

  #class variable
  PRINT=["major", "minor", "file"]

  # --------------------------------------
  def __init__(self, major, minor, file):
    """
    initialise instance variables
    """
    Metadata.__init__(self)
    self.major = major
    self.minor = minor
    self.file = file
    self.constants = SpecContainer()
    self.classes = SpecContainer()
    # methods indexed by classname_methname
    self.methods = {}

  # -------------------
  def post_load(self):
    """
    creates a module and class object
    """
    self.module = self.define_module("amqp%s%s" % (self.major, self.minor))
    self.klass = self.define_class("Amqp%s%s" % (self.major, self.minor))

  # ----------------------
  def method(self, name):
    """
    ? - dosen't seem to be used anywhere currently ...
    """
    if not self.methods.has_key(name):
      for cls in self.classes:
        clen = len(cls.name)
        if name.startswith(cls.name) and name[clen] == "_":
          end = name[clen + 1:]
          if cls.methods.byname.has_key(end):
            self.methods[name] = cls.methods.byname[end]
    return self.methods.get(name)

  # ----------------------------
  def parse_method(self, name):
    """
    ? - dosen't seem to be used anywhere currently ...
    """
    parts = re.split(r"\s*\.\s*", name)
    if len(parts) != 2:
      raise ValueError(name)
    klass, meth = parts
    return self.classes.byname[klass].methods.byname[meth]

  # -----------------------------------------
  def define_module(self, name, doc = None):
    """
    creates a module object, encapsulating all the classes found in the xml spec
    """
    module = new.module(name, doc)
    module.__file__ = self.file
    for c in self.classes:
      cls = c.define_class(c.name)
      cls.__module__ = module.__name__
      setattr(module, c.name, cls)
    return module

  # ----------------------------
  def define_class(self, name):
    """
    creates a class type, containing all the required methods
    """
    methods = {}
    for c in self.classes:
      for m in c.methods:
        meth = m.klass.name + "_" + m.name
        methods[meth] = m.define_method(meth)
    return type(name, (), methods)

# ------------------------
# ------------------------
class Constant(Metadata):
  """
  class encpsulating all 'constant' tag data
  """

  PRINT=["name", "id"]

  # ------------------------------------------------
  def __init__(self, spec, name, id, klass, docs):
    """
    initializations...
    """
    Metadata.__init__(self)
    self.spec = spec
    self.name = name
    self.id = id
    self.klass = klass
    self.docs = docs

# ---------------------
# ---------------------
class Class(Metadata):
  """
  class encpsulating all 'class' tag data
  """

  PRINT=["name", "id"]

  # -------------------------------------------------
  def __init__(self, spec, name, id, handler, docs):
    """
    initializations...
    """
    Metadata.__init__(self)
    self.spec = spec
    self.name = name
    self.id = id
    self.handler = handler
    self.fields = SpecContainer()
    self.methods = SpecContainer()
    self.docs = docs

  # ----------------------------
  def define_class(self, name):
    """
    creates a class type, containing all the required methods
    """
    methods = {}
    for m in self.methods:
      methods[m.name] = m.define_method(m.name)
    return type(name, (), methods)

# ----------------------
# ----------------------
class Method(Metadata):
  """
  class encpsulating all 'method' tag data
  """

  PRINT=["name", "id"]

  # -------------------------------------------------------------------
  def __init__(self, klass, name, id, content, responses, synchronous,
               description, docs):
    """
    initializations...
    """
    Metadata.__init__(self)
    self.klass = klass
    self.name = name
    self.id = id
    self.content = content
    self.responses = responses
    self.synchronous = synchronous
    self.fields = SpecContainer()
    self.description = description
    self.docs = docs
    self.response = False

  # ------------------------------------
  def arguments(self, *args, **kwargs):
    """
    returns a tuple of arguments in a manner that can be used by the method object invoking this method
    the 'fields' property of this class contains the list of fields required by this method in the right order.
    this function massages the input argument list to match the defined order and returns a tuple of it.
    """
    nargs = len(args) + len(kwargs)
    maxargs = len(self.fields)
    if nargs > maxargs:
      self._type_error("takes at most %s arguments (%s) given", maxargs, nargs)
    result = []
    for f in self.fields:
      idx = self.fields.index(f)
      if idx < len(args):
        result.append(args[idx])
      elif kwargs.has_key(f.name):
        result.append(kwargs.pop(f.name))
      else:
        result.append(Method.DEFAULTS[f.type])
    for key, value in kwargs.items():
      if self.fields.byname.has_key(key):
        self._type_error("got multiple values for keyword argument '%s'", key)
      else:
        self._type_error("got an unexpected keyword argument '%s'", key)
    return tuple(result)

  # ---------------------------------
  def _type_error(self, msg, *args):
    """
    called by the 'arguments' method to indicate that the supplied arguments did not match the method signature
    """
    raise TypeError("%s %s" % (self.name, msg % args))

  # -------------------
  def docstring(self):
    """
    places the contents in the 'doc' tag of the method definition from the xml specification document into the methods
    docstring
    """
    s = "\n\n".join([fill(d, 2) for d in [self.description] + self.docs])
    for f in self.fields:
      if f.docs:
        s += "\n\n" + "\n\n".join([fill(f.docs[0], 4, f.name)] +
                                  [fill(d, 4) for d in f.docs[1:]])
    if self.responses:    
      s += "\n\nValid responses: "    
      for r in self.responses:
        s += r.name + " "
    return s

  METHOD = "__method__"
  DEFAULTS = {"bit": False,
              "shortstr": "",
              "longstr": "",
              "table": {},
              "octet": 0,
              "short": 0,
              "long": 0,
              "longlong": 0,
              "timestamp": 0,
              "content": None}

  # -----------------------------
  def define_method(self, name):
    """
    returns a code object for a method named 'name'
    """

    self.__dict__['__doc__'] = self.docstring()

    g = {Method.METHOD: self}
    l = {}
    args = [(f.name, Method.DEFAULTS[f.type]) for f in self.fields]
    methargs = args[:]
    if self.content:
      args += [("content", None)]
    code = "def %s(self, %s):\n" % \
           (name, ", ".join(["%s = %r" % a for a in args]))
    code += "  %r\n" % self.docstring()
    argnames = ", ".join([a[0] for a in methargs])
    code += "  return self.invoke(%s" % Method.METHOD
    if argnames:
      code += ", (%s,)" % argnames
    else:
      code += ", ()" 
    if self.content:
      code += ", content"
    code += ")"
    exec code in g, l
    return l[name]

# ---------------------
# ---------------------
class Field(Metadata):
  """
  class encpsulating all 'field' tag data
  """

  PRINT=["name", "id", "type"]

  # ----------------------------------------
  def __init__(self, name, id, type, docs):
    """
    initializations...
    """
    Metadata.__init__(self)
    self.name = name
    self.id = id
    self.type = type
    self.docs = docs

# ----------------
def get_docs(nd):
  """
  returns the contents of the 'doc' child tag of the node 'nd'
  """
  return [n.text for n in nd["doc"]]

# -------------------------------
def load_fields(nd, l, domains):
  """
  Loads the class fields into the class.fields SpecContainer
  """
  for f_nd in nd["field"]:
    try:
      type = f_nd["@domain"]
    except KeyError:
      type = f_nd["@type"]
    while domains.has_key(type) and domains[type] != type:
      type = domains[type]
    l.add(Field(pythonize(f_nd["@name"]), f_nd.index(), type, get_docs(f_nd)))

# ---------------------------
def load(specfile, *errata):
  """
  interface to the outside world
  
  traverses the specfile, and creates object representations of the tags such as constants, fields
  class and so on. These are placed into the Spec object.
  """
  doc = xmlutil.parse(specfile)
  spec_root = doc["amqp"][0]
  spec = Spec(int(spec_root["@major"]), int(spec_root["@minor"]), specfile)

  for root in [spec_root] + map(lambda x: xmlutil.parse(x)["amqp"][0], errata):
    # constants
    for nd in root["constant"]:
      const = Constant(spec, pythonize(nd["@name"]), int(nd["@value"]),
                       nd.get("@class"), get_docs(nd))
      spec.constants.add(const)

    # domains are typedefs
    domains = {}
    for nd in root["domain"]:
      domains[nd["@name"]] = nd["@type"]

    # classes
    for c_nd in root["class"]:
      cname = pythonize(c_nd["@name"])
      if root == spec_root:
        klass = Class(spec, cname, int(c_nd["@index"]), c_nd["@handler"],
                      get_docs(c_nd))
        spec.classes.add(klass)
      else:
        klass = spec.classes.byname[cname]

      added_methods = []
      load_fields(c_nd, klass.fields, domains)
      for m_nd in c_nd["method"]:
        mname = pythonize(m_nd["@name"])
        if root == spec_root:
          meth = Method(klass, mname,
                        int(m_nd["@index"]),
                        m_nd.get_bool("@content", False),
                        [pythonize(nd["@name"]) for nd in m_nd["response"]],
                        m_nd.get_bool("@synchronous", False),
                        m_nd.text,
                        get_docs(m_nd))
          klass.methods.add(meth)
          added_methods.append(meth)
        else:
          meth = klass.methods.byname[mname]
        load_fields(m_nd, meth.fields, domains)
      # resolve the responses
      for m in added_methods:
        m.responses = [klass.methods.byname[r] for r in m.responses]
        for resp in m.responses:
          resp.response = True

  spec.post_load()
  return spec

REPLACE = {" ": "_", "-": "_"}
KEYWORDS = {"global": "global_",
            "return": "return_"}

# -------------------
def pythonize(name):
  """
  Converts spaces(' ') and hypens('-') to underscores('_')
  Also performs keyword replacements e.g global is changed to global_ etc
  """
  name = str(name)
  for key, val in REPLACE.items():
    name = name.replace(key, val)
  try:
    name = KEYWORDS[name]
  except KeyError:
    pass
  return name

# --------------------------------------
def fill(text, indent, heading = None):
  """
  returns data in the form:
  heading -- text
  the above is text wrapped to a default width of 70
  """
  sub = indent * " "
  if heading:
    init = (indent - 2) * " " + heading + " -- "
  else:
    init = sub
  w = textwrap.TextWrapper(initial_indent = init, subsequent_indent = sub)
  return w.fill(" ".join(text.split()))

# --------------------
# --------------------
class Rule(Metadata):
  """
  class encapsulating the 'rule' tag of the xml specification doc
  """

  PRINT = ["text", "implement", "tests"]

  # ------------------------------------------------
  def __init__(self, text, implement, tests, path):
    """
    initializations ...
    """
    self.text = text
    self.implement = implement
    self.tests = tests
    self.path = path

# ----------------------------
def find_rules(node, rules):
  """
  ? - dosen't seem to be used
  """
  if node.name == "rule":
    rules.append(Rule(node.text, node.get("@implement"),
                      [ch.text for ch in node if ch.name == "test"],
                      node.path()))
  if node.name == "doc" and node.get("@name") == "rule":
    tests = []
    if node.has("@test"):
      tests.append(node["@test"])
    rules.append(Rule(node.text, None, tests, node.path()))
  for child in node:
    find_rules(child, rules)

# ------------------------
def load_rules(specfile):
  """
  ? - dosen't seem to be used
  """
  rules = []
  find_rules(xmlutil.parse(specfile), rules)
  return rules

# ------------------
def test_summary():
  """
  ? - dosen't seem to be used
  """
  template = """
  <html><head><title>AMQP Tests</title></head>
  <body>
  <table width="80%%" align="center">
  %s
  </table>
  </body>
  </html>
  """
  rows = []
  for rule in load_rules("amqp.org/specs/amqp7.xml"):
    if rule.tests:
      tests = ", ".join(rule.tests)
    else:
      tests = "&nbsp;"
    rows.append('<tr bgcolor="#EEEEEE"><td><b>Path:</b> %s</td>'
                '<td><b>Implement:</b> %s</td>'
                '<td><b>Tests:</b> %s</td></tr>' %
                (rule.path[len("/root/amqp"):], rule.implement, tests))
    rows.append('<tr><td colspan="3">%s</td></tr>' % rule.text)
    rows.append('<tr><td colspan="3">&nbsp;</td></tr>')

  print template % "\n".join(rows)
 

