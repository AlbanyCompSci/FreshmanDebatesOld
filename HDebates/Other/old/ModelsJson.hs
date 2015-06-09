module ModelsJson where
-- TODO: Can these instances be made elegantly with Template Haskell

import Data.Aeson (FromJSON, ToJSON, Object, String)

import Models ( Debate
              , DebateItem
              , Evaluation
              , Score
              , Section
              , Team
              , User
              )

instance FromJSON Debate where
    parseJSON (Object v) =  Person
                        <$> v .: "id"
                        <*> v .: "title"
                        <*> v .: "location"
                        <*> v .: "judges"
                        <*> v .: "affirmative team"
                        <*> v .: "negative team"
                        <*> v .: "affirmative scores"
                        <*> v .: "negative scores"
    parseJSON _ = mzero
instance ToJSON Debate where
    toJSON d = object
               [ "id"                 .= did       d
               , "title"              .= title     d
               , "location"           .= location  d
               , "judges"             .= judges    d
               , "affirmative team"   .= affTeam   d
               , "negative team"      .= negTeam   d
               , "affirmative scores" .= affScores d
               , "negative scores"    .= negScores d
               ]

instance FromJSON User where
    parseJSON (Object v) = User <$> v .: "id"
    parseJSON _          = mempty
instance ToJSON User where
    toJSON u = object [ "id" .= uid u ]

instance FromJSON Team where
    parseJSON (Object v) =  Team
                        <$> v .: "id"
                        <*> v .: "teachers"
                        <*> v .: "students"
    parseJSON _ = mempty
instance ToJSON Team where
    toJSON t = object
               [ "id"       .= tid      t
               , "teachers" .= teachers t
               , "students" .= students t
               ]

instance FromJSON DebateItem where
    parseJSON (String v) = pure $ read v
    parseJSON _          = mempty
instance ToJSON DebateItem where
    toJSON = String . show

instance FromJSON (Map User Score) where
    parseJSON = fmap (mapKeys (User . read)) . parseJSON
instance ToJSON (Map User Score) where
    toJSON = toJSON . mapKeys (show . uid)

instance FromJSON (Map DebateItem Evaluation) where
    parseJSON = fmap (mapKeys read) . parseJSON
instance ToJSON (Map DebateItem Evaluation) where
    toJSON = toJSON . mapKeys show

instance FromJSON Evaluation where
    parseJSON (Object v) =  Evaluation
                        <$> v .: "id"
                        <*> v .: "score"
                        <*> v .: "notes"
    parseJSON _ = mempty
instance ToJSON Evaluation where
    toJSON e = object
               [ "id"    .= eid   e
               , "score" .= score e
               , "notes" .= notes e
               ]
