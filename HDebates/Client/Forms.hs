{-# LANGUAGE OverloadedStrings #-}

module Forms ( Form ) where

import Data.Monoid ((<>))

import Text.Blaze.Html             (Html, toHtml)
import Text.Blaze.Html5            (input, select, value)
import Text.Blaze.Html5.Attributes (type_, value)

import Shared.Models (Debate, User, Team, Score, DebateItem)
import Client.Api    (getLocations, getJudges, getTeams, getStudents)

class Form a where
    toForm   :: a -> IO Html
    fromForm :: _ -> a

textLine :: Html
textLine = input ! type_ "text"

textBox :: Html
textLine = input ! type_ "text"

timeSelect :: Html
timeSelect = input ! type_ "time"

emailLine :: Html
emailLine = input ! type_ "email"

selectBox :: Show a => [a] -> Html
selectBox = select . foldMap ((\s -> option ! value s $ toHtml s) . show)

label :: Html -> Html
label = undefined

instance Form Debate where
    toForm d = do
        ls <- getLocations
        js <- getJudges
        ts <- getTeams
        H.form $ mconcat
        [ label "Title"            $ textLine     $ title    d
        , label "Time"             $ timeSelect   $ time     d
        , label "Location"         $ selectBox ls $ location d
        , label "Judges"           $ selectBox js $ judges   d
        , label "Affirmative Team" $ selectBox ts $ affTeam  d
        , label "Negative Team"    $ selectBox ts $ negTeam  d
        ]
    fromForm d

instance Form User where
    toForm u = return $ H.form $ mconcat
               [ label "First Name" $ textLine  $ firstName u
               , label "Last Name"  $ textLine  $ lastName  u
               , label "Email"      $ emailLine $ email     u
               ]
    fromForm u =

instance Form Team where
    toForm t = do
        ts <- getTeachers
        ss <- getStudents
        H.form $ mconcat
        [ label "Teachers" $ selectBox ts $ teachers t
        , label "Students" $ selectBox ss $ students t
        ]
    fromForm u =

instance Form (Score) where
    toForm = return $ H.form $ mconcat
           $ map (\i -> label (show i) $ evaluationBox)
           $ (enumFrom (fromEnum 0) :: DebateItem)
      where evaluationBox = selectBox [1..10] <> textBox
