'''
List-type functions for Jeeves containers.
'''
import JeevesLib
from fast.AST import FExpr, Constant, Facet

@JeevesLib.supports_jeeves
def jhasElt(lst, f):
  if isinstance(lst, Facet):
    return JeevesLib.jif(lst.cond, lambda:jhasElt(lst.thn, f), lambda:jhasElt(lst.els, f))
  elif isinstance(lst, JeevesLib.JList):
    return jhasElt(lst.l, f)
  elif isinstance(lst, JeevesLib.FObject):
    return jhasElt(lst.v, f)

  acc = False
  # Short circuits.
  for elt in lst:
    isElt = f(elt) # TODO: This should eventually be japply of f to elt.
    if isinstance(isElt, FExpr):
      acc = JeevesLib.jor(lambda: isElt, lambda: acc)
    else:
      if isElt:
        return True
  return acc

@JeevesLib.supports_jeeves
def jhas(lst, v):
  return jhasElt(lst, lambda x: x == v)

@JeevesLib.supports_jeeves
def jall(lst):
  def myall(lst):
    acc = True
    for elt in lst:
      acc = JeevesLib.jand(lambda: elt, lambda: acc)
    return acc

  if isinstance(lst, list):
    return myall(lst)
  else: # lst is a JList
    return JeevesLib.facetMapper(lst.l, myall)
