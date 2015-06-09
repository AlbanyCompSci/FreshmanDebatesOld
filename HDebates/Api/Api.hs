{-# LANGUAGE OverloadedStrings #-}

module Api.Main(main) where

import Rest.Api

import Resources as Resources

main :: IO ()
main = do
    runSqlite ":memory:" $ runMigration migrateAll
    st <- initialState
    run 3000 $ apiToApplication (runApi st) api

api :: Api IO
api = [(mkVersion 1 0 0, Some1 debates)]

debates :: Router IO IO
debates = root -/ debate
                 --/ score
                   ---/ evaluation
               -/ team
               -/ user
  where
    debate     = route Resources.debate
    score      = route Resources.score
    evaluation = route Resources.evaluation
    team       = route Resources.team
    user       = route Resources.user

runApi :: ServerData -> ApiState a -> IO a
runApi sd =
