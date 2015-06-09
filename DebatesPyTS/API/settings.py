DEBUG = True

MONGO_HOST     = 'localhost'
MONGO_PORT     = 27017
MONGO_USERNAME = 'api'
MONGO_PASSWORD = 'test'
MONGO_DBNAME   = 'api'

RESOURE_METHODS = ['GET', 'POST', 'DELETE']

ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

def listOf(t):
    return { 'type'   : 'list'
           , 'schema' : { 'type' : t }
           }

def dictOf(t):
    return { 'type'      : 'dict'
           , 'keyschema' : { 'type' : t }
           }

class SproxyAuth(BasicAuth):
    def authorized(self, allowed_roles, resource, method):
        email = request.headers['From']
        user = app.data.driver.db['users'].find_one({ 'email' : email })
        action = Action(request.method, request.url)
        return self.isAuth(user, action)
    def isAuth(self, user, action):
        raise NotImplementedError("Must be defined at the resource level")

class Act(Enum):
    read   = 'GET'
    create = 'POST'
    update = 'PATCH'
    delete = 'DELETE'

class Action(object):
    def __init__(self, method, url):
        self.type = method

debateSchema = { 'title'     : { 'type' : 'string'           }
               , 'time'      : { 'type' : 'datetime'         }
               , 'location'  : { 'type' : 'string'           }
               , 'judges'    : { 'type' : listOf('objectid') }
               , 'affTeam'   : { 'type' : 'objectid'         }
               , 'negTeam'   : { 'type' : 'objectid'         }
               , 'affScores' : { 'type' : dictOf('objectid') }
               , 'negScores' : { 'type' : dictOf('objectid') }
               }
class DebateAuth(SproxyAuth):
    def isAuth(self, user, action):
        if action.type in [Act.create,Act.update,Act.delete]:
            return isAdmin(user)
        if action.type is Act.read:
            debate = action.item
            participants = set(teamUsers(debate.affTeam)) |
                           set(teamUsers(debate.negTeam)) |
                           set(debate.judges)
            return user in participants:
                return True
            return False
        if action.type is 'DELETE':
debates = { 'item_title': 'debate'
          , 'resource_methods': ['GET','POST']
          , 'schema': debateSchema
          , 'authentication': DebateAuth
          }

evaluationSchema = { 'score' : { 'type' : 'integer'
                               , 'min' : 0
                               , 'max' : 10
                               }
                   , 'notes' : { 'type' : 'string' }
                   }
evaluations = { 'item_title': 'evaluation'
              , 'resource_methods': ['GET','POST']
              , 'schema': evaluationSchema
              }

scoreSchema = { 'speakerA'  : { 'type' : 'objectid' }
              , 'speakerB'  : { 'type' : 'objectid' }
              , 'crossExam' : { 'type' : 'objectid' }
              , 'slideShow' : { 'type' : 'objectid' }
              , 'rebuttal'  : { 'type' : 'objectid' }
              , 'argument'  : { 'type' : 'objectid' }
              }
scores = { 'item_title': 'score'
         , 'resource_methods': ['GET','POST']
         , 'schema': scoreSchema
         }

teamSchema = { 'teachers' : { 'type' : listOf('objectid') }
             , 'debaters' : { 'type' : listOf('objectid') }
             }
teams = { 'item_title': 'team'
        , 'resource_methods': ['GET','POST']
        , 'schema': scoreSchema
        }

userSchema = { 'email' : { 'type' : 'string', 'unique' : True } }
users = { 'item_title': 'user'
        , 'resource_methods': ['GET','POST']
        , 'schema': userSchema
        }

DOMAIN = { 'debates'     : debates
         , 'evaluations' : evaluations
         , 'scores'      : scores
         , 'teams'       : teams
         , 'users'       : users
         }
