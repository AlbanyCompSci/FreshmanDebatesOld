TIME_FORMAT = '%Y-%m-%dT%H:%M:%S' # UTC format

# NOTE: read is a static method creating a new object

class Debate(object, JSONEncoder):
    def parse(form):
        debate = Debate()
        debate.title     = str(form['title'])
        debate.time      = datetime.strptime(form['time'], TIME_FORMAT)
        debate.location  = str(form['location'])
        debate.judges    = map(int, form['judges'])
        debate.affTeam   = int(form['affTeam'])
        debate.negTeam   = int(form['negTeam'])
        debate.affScores = map(int, form['affScores'])
        debate.negScores = map(int, form['negScores'])
        return debate
    def format(self):
        return { 'title'     : str(self['title'])
               , 'time'      : self.time.strftime(TIME_FORMAT)
               , 'location'  : str(self.location)
               , 'judges'    : map(int, form['judges'])
               , 'affTeam'   : int(form['affTeam'])
               , 'negTeam'   : int(form['negTeam'])
               , 'affScores' : map(int, form['affScores'])
               , 'negScores' : map(int, form['negScores'])
               }

class Evaluation(object):
    def parse(form):
        evaluation = Evaluation()
        evaluation.score = float(form['score'])
        evaluation.notes = str(form['notes'])
        return evaluation
    def format(self):
        return { 'score' : str(self.score)
               , 'notes' : str(self.notes)
               }

class Score(object):
    def parse(form):
        score = Score()
        score.speakerA  = int(form['speakerA'])
        score.speakerB  = int(form['speakerB'])
        score.crossExam = int(form['crossExam'])
        score.slideShow = int(form['slideShow'])
        score.rebuttal  = int(form['rebuttal'])
        score.argument  = int(form['argument'])
        return score
    def format(self):
        return { 'speakerA'  : int(score.speakerA)
               , 'speakerB'  : int(score.speakerB)
               , 'crossExam' : int(score.crossExam)
               , 'slideShow' : int(score.slideShow)
               , 'rebuttal'  : int(score.rebuttal)
               , 'argument'  : int(score.argument)
               }
