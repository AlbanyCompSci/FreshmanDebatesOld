from flask import Flask
from flask.ext.restful import Api

import Types
from Database import DebatesDatabase
import Resources as Rs

app = Flask(__name__)
api = Api(app)

db = DebatesDatabase.open('debates.db')

Rs.addResource(api, db, Types.Debate,     'debates'    )
Rs.addResource(api, db, Types.Score,      'scores'     )
Rs.addResource(api, db, Types.Evaluation, 'evaluations')
Rs.addResource(api, db, Types.Team,       'teams'      )
Rs.addResource(api, db, Types.User,       'users'      )

if __name__ == '__main__':
    app.run(debug=True)
