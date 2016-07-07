# {# pkglts, base

from . import version

__version__ = version.__version__

# #}

# CPL: Do not import anything in the __init__
# Otherelse it may breaks everything see commit  15337

from utils import IdDict
from data_prop import Quantity, DataProp
from graph import Graph
from grid import Grid
from property_graph import PropertyGraph
from relation import Relation
from tree import Tree, PropertyTree

################################
#
#       mesh
#
################################
from topomesh import *
from topomesh_txt import write_topomesh, read_topomesh
from topomesh_algo import *
from topomesh_geom_algo import *

from array_dict import array_dict
from property_topomesh import PropertyTopomesh
