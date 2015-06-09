module Models
    ( Debate
    , DebateItem
    , Evaluation
    , Score
    , Section
    , Team
    , User
    ) where

import Data.Time (UTCTime)
import Data.Text (Text)

data Debate = Debate { did       :: Int
                     , title     :: String
                     , time      :: UTCTime
                     , location  :: String
                     , judges    :: [User]
                     , affTeam   :: Team
                     , negTeam   :: Team
                     , affScores :: ScoreSet
                     , negScores :: ScoreSet
                     }

data User = User { uid   :: Int } deriving (Eq, Ord)

data Team = Team { tid      :: Int
                 , teachers :: [User]
                 , students :: [User]
                 }

data DebateItem = SpeakerA
                | SpeakerB
                | CrossExam
                | SlideShow
                | Rebuttal
                | Argument
                deriving (Show, Read, Eq)

-- maps a judge to a score they gave
type ScoreSet = Map User Score

type Score = Map DebateItem Evaluation

data Evaluation = Evaluation { eid   :: Int
                             , score :: Int
                             , notes :: Text
                             }
