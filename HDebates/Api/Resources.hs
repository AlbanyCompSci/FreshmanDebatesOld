module HDebates.Resources
  ( debate
  , score
  , evaluation
  , team
  , user
  ) where

newtype Res a = Res { name :: String }

get :: Res a -> Handler (ReaderT Id IO)
get res = mkHandler (jsonO . authHeader) $ \env -> do
          id <- ask
          ofType res $ authLookup (header env) id

list :: Res a -> ListHandler IO
list res = mkGenHandler (jsonO . authHeader) $ \env ->
           ofType res $ authList (headerenv)

update :: Res a -> Handler (ReaderT Id IO)
delete :: Res a -> Handler (ReaderT Id IO)
create :: Res a -> Handler (ReaderT Id IO)

mkNamedResource :: String -> Resource IO (ReaderT Id IO) Id () Void
mkNamedResource res = mkResourceReader
    { R.name   = name res
    , R.schema = withListing () $ named [("id", singleBy id)]
    , R.list   = const list
    , R.get    = Just $ get    res
    , R.update = Just $ update res
    , R.remove = Just $ remove res
    , R.create = Just $ create res
    }

debate     = mkNamedResource (Res "debate"     :: Res Debate    )
score      = mkNamedResource (Res "score"      :: Res Score     )
evaluation = mkNamedResource (Res "evaluation" :: Res Evaluation)
team       = mkNamedResource (Res "team"       :: Res Team      )
user       = mkNamedResource (Res "user"       :: Res User      )
