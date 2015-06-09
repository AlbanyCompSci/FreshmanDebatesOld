-- file: Vote.hs
-- defines a vote datatype for elections

data Ballot = Ballot [Issue]
data Vote = Vote [(Issue,Descision)]
data Issue = Issue { title       :: String
                   , description :: String
                   , option      :: Option
                   }

class Option a where
    data Descision a :: *
    writeForm :: a -> Form
    readForm :: Form -> Descision a
    store :: ()

data YesNo

instance Option YesNo where
    data Descision YesNo = Bool

data Candidate = Candidate { name :: String, affiliation :: String }
data SingleCandidate = SingleCandidate [Candidate]

instance Option SingleCandidate where
    data Descision SingleCandidate = Int

myBallot :: Ballot
myBallot = Ballot [governor, prop1, prop2, prop45, prop46, prop47, prop48]
    where governor = Issue "Governor" "Race for governor of California"
                     $ SingleCandidate [jerryBrown, neelKashkari]
          jerryBrown = Candidate "Edmund G. \"Jerry\" Brown" "Democrat"
          neelKashkari = Candidate "Neel Kashkari" "Republican"
          prop1 = prop 1 "Water bond. Funding for water quality, supply, treatment, and storage projects."
          prop2 = prop 2 "State budget. Budget stabilization account."
          prop45 = prop 45 "Healthcare insurance. Rate changes."
          prop46 = prop 46 "Drug and alcohol testing of doctors. Medical negligence lawsuits."
          prop47 = prop 47 "Criminal sentences. Misemeanor penalties."
          prop48 = prop 48 "Indian gaming compacts. Referendum."
          prop :: Int -> String -> Issue
          prop n desc = Issue ("Proposition " ++ show n) desc YesNo
