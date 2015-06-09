{-# LANGUAGE EmptyDataDecls             #-}
{-# LANGUAGE FlexibleContexts           #-}
{-# LANGUAGE GADTs                      #-}
{-# LANGUAGE GeneralizedNewtypeDeriving #-}
{-# LANGUAGE MultiParamTypeClasses      #-}
{-# LANGUAGE OverloadedStrings          #-}
{-# LANGUAGE QuasiQuotes                #-}
{-# LANGUAGE TemplateHaskell            #-}
{-# LANGUAGE TypeFamilies               #-}

module Models
    ( Debate
    , DebateItem
    , Evaluation
    , Score
    , Section
    , Team
    , User
    ) where

-- import           Control.Monad.IO.Class  (liftIO)
import           Database.Persist
import           Database.Persist.Sqlite
import           Database.Persist.TH

import qualified Data.Text as Text

instance (Show k, Read k, PersistField v) => PersistField (Map k v) where
    toPersistValue   m = toPersistValue $ mapKeys (Text.pack . show) m
    fromPersistValue m = mapKeys (read . Text.unpack) $ fromPersistValue m

data DebateItem = SpeakerA
                | SpeakerB
                | CrossExam
                | SlideShow
                | Rebuttal
                | Argument
                deriving (Show, Read, Eq)
derivePersistField "DebateItem"

-- maps a judge to a score they gave
type ScoreSet    = Map UserId ScoreId
type ScoreFields = Map DebateItem Evaluation

share [mkPersist sqlSettings, mkMigrate "migrateAll"] [persistLowerCase|
Debate json
    title     String
    time      UTCTime
    location  String
    judges    [UserId]
    affTeam   TeamId
    negTeam   TeamId
    affScores ScoreSet
    negScores ScoreSet
Evaluation json
    score Int
    notes Text
Score json
    fields ScoreFields
Team json
    teachers [UserId]
    students [UserId]
User json
    firstName String
    lastName  String
    email     String
|]
