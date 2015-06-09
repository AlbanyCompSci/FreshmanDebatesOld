-- Module for dealing with authentication using details from the Sproxy server

module Auth
  ( AuthDetails
    ( from
    , groups
    , givenName
    , familyName
    , forwardedFor
    )
  , authHeader
  ) where

import Rest.Dictionary (Dict, Header(Header), mkHeader)
import Rest.Types.Error (DataError(MissingField,ParseError))

data AuthDetails = AuthDetails
                 { from         :: String
                 , groups       :: String
                 , givenName    :: String
                 , familyName   :: String
                 , forwardedFor :: String
                 }

authHeader :: Dict x p i o e -> Dict AuthDetails p i o e
authHeader = mkHeader $ Header fields parser
  where
    fields :: [String]
    fields = [ "From"
             , "X-Groups"
             , "X-Given-Name"
             , "X-Family-Name"
             , "X-Forwarded-For"
             ]
    parser :: [Maybe String] -> Either DataError AuthDetails
    parser fs =  AuthDetails
             <$> get fs 1 "From"
             <*> get fs 2 "X-Groups"
             <*> get fs 3 "X-Given-Name"
             <*> get fs 4 "X-Family-Name"
             <*> get fs 5 "X-Forwarded-For"
    get :: [Maybe String] -> Int -> String -> Either DataError String
    get fs i field = case atMay fs i of
                          Nothing -> Left $ MissingField field
                          Just h  -> case h of
                                          Nothing -> Left $ ParseError field
                                          Just s  -> Right s
