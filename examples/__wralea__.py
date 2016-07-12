from openalea.core import CompositeNodeFactory as CNF

__name__ = 'openalea.container.example'

__editable__ = True
__description__ = ''
__license__ = ''
__url__ = ''
__alias__ = []
__version__ = ''
__authors__ = 'Jerome Chopard'
__institutes__ = ''
__icon__ = ''

__all__ = ['cnf']

cnf = CNF(name='simple_mesh_use',
          description='nothing really important there',
          category='experimental hardcore',
          doc='',
          inputs=[],
          outputs=[],
          elt_factory={2: (
              'openalea.container.mesh',
              'clean_geometry'),
              3: ('openalea.container.mesh', 'add_wisp'),
              4: ('openalea.container.mesh', 'remove_wisp'),
              5: ('openalea.container.mesh', 'clean_orphans')},
          elt_connections={14184928: (2, 0, 5, 0),
                           14184952: (4, 0, 2, 0),
                           14184976: (3, 0, 4, 0)},
          elt_data={2: {'block': False,
                        'caption': 'clean_geometry',
                        'delay': 0,
                        'hide': True,
                        'id': 2,
                        'lazy': True,
                        'port_hide_changed': set([]),
                        'posx': 11.830011254049865,
                        'posy': 69.0083989819576,
                        'priority': 0,
                        'use_user_color': False,
                        'user_application': None,
                        'user_color': None},
                    3: {'block': False,
                        'caption': 'add_wisp',
                        'delay': 0,
                        'hide': True,
                        'id': 3,
                        'lazy': True,
                        'port_hide_changed': set([]),
                        'posx': -25.35339157950071,
                        'posy': -50.706783159001404,
                        'priority': 0,
                        'use_user_color': False,
                        'user_application': None,
                        'user_color': None},
                    4: {'block': False,
                        'caption': 'remove_wisp',
                        'delay': 0,
                        'hide': True,
                        'id': 4,
                        'lazy': True,
                        'port_hide_changed': set([]),
                        'posx': -0.18734074432035186,
                        'posy': 7.00452428841356,
                        'priority': 0,
                        'use_user_color': False,
                        'user_application': None,
                        'user_color': None},
                    5: {'block': False,
                        'caption': 'clean_orphans',
                        'delay': 0,
                        'hide': True,
                        'id': 5,
                        'lazy': True,
                        'port_hide_changed': set([]),
                        'posx': 20.70251969458728,
                        'posy': 136.04512942157356,
                        'priority': 0,
                        'use_user_color': False,
                        'user_application': None,
                        'user_color': None},
                    '__in__': {'block': False,
                               'caption': 'In',
                               'delay': 0,
                               'hide': True,
                               'id': 0,
                               'lazy': True,
                               'port_hide_changed': set([]),
                               'posx': 0,
                               'posy': 0,
                               'priority': 0,
                               'use_user_color': True,
                               'user_application': None,
                               'user_color': None},
                    '__out__': {'block': False,
                                'caption': 'Out',
                                'delay': 0,
                                'hide': True,
                                'id': 1,
                                'lazy': True,
                                'port_hide_changed': set([]),
                                'posx': 0,
                                'posy': 0,
                                'priority': 0,
                                'use_user_color': True,
                                'user_application': None,
                                'user_color': None}},
          elt_value={2: [],
                     3: [(0, 'None'), (1, '0'),
                         (2, 'None')],
                     4: [(1, '0'), (2, '0')],
                     5: [],
                     '__in__': [],
                     '__out__': []},
          elt_ad_hoc={2: {
              'position': [11.830011254049865,
                           69.0083989819576],
              'userColor': None,
              'useUserColor': False},
              3: {'position': [
                  -25.35339157950071,
                  -50.706783159001404],
                  'userColor': None,
                  'useUserColor': False},
              4: {'position': [
                  -0.18734074432035186,
                  7.00452428841356],
                  'userColor': None,
                  'useUserColor': False},
              5: {'position': [
                  20.70251969458728,
                  136.04512942157356],
                  'userColor': None,
                  'useUserColor': False},
              '__in__': {
                  'position': [0, 0],
                  'userColor': None,
                  'useUserColor': True},
              '__out__': {
                  'position': [0, 0],
                  'userColor': None,
                  'useUserColor': True}},
          lazy=True,
          eval_algo='LambdaEvaluation',
          )