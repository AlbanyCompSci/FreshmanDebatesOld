module DB where

import Database.Persist.Class (get, insert, selectList, replace)

type Id = Int64

data Action a = Read   item
              | Write  old new
              | Create new
              | Delete old

class Protected a where
    policy :: Action a -> AuthDetails -> Maybe (Action a)

authGet :: Protected a => AuthDetails -> Id -> ErrorT (Reason e) IO (Identity a)
authGet ad id = do
    mayItem <- get $ toSqlKey id
    case mayItem of
         Nothing   -> NotFound
         Just item -> case policy (Read item) ad of
                           Nothing   -> NotAllowed
                           Just item -> liftIO $ return item


authList :: Protected a => AuthDetails -> ErrorT (Reason e) IO [a]
authList ad =  liftIO
            $  catMaybes . map (\i -> policy (Read i) ad) items
           <$> selectList [] []

authUpdate :: Protected a => AuthDetails -> Id -> a -> ErrorT (Reason e) IO ()
authUpdate ad id new = do
    mayOld <- get $ toSqlKey id
    case mayOld of
         Nothing  -> NotFound
         Just old -> case policy (Write old new) ad of
                          Nothing   -> NotAllowed
                          Just item -> liftIO $ replace (toSqlKey id) item

authDelete :: Protected a => AuthDetails -> Id -> ErrorT (Reason e) IO ()
authDelete ad id = do
    mayOld <- get $ toSqlKey id
    case mayOld of
         Nothing  -> NotFound
         Just old -> case policy (Delete old) ad of
                          Nothing   -> NotAllowed
                          Just item -> liftIO $ delete $ toSqlKey id

authCreate :: Protected a => AuthDetails -> a -> ErrorT (Reason e) IO Id
authCreate ad new = case policy (Create new) ad of
                         Nothing   -> NotAllowed
                         Just item -> liftIO $ fromSqlKey <$> insert new
