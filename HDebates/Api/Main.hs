{-# LANGUAGE OverloadedStrings #-}
module Main (main) where

import Network.Wai.Handler.Warp
import Rest.Driver.Wai (apiToApplication)

import Api (api)
import ApiTypes (runBlogApi)
import Example (exampleBlog)

main :: IO ()
main = do
    -- Set up the server state for the blog and start warp.
    runMigration migrateAll
    putStrLn "Starting warp server on http://localhost:3000"
    serverData <- getDatabase
    run 3000 $ apiToApplication (runApi serverData) api
