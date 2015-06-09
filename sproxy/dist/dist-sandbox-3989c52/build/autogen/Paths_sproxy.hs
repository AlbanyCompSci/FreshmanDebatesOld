module Paths_sproxy (
    version,
    getBinDir, getLibDir, getDataDir, getLibexecDir,
    getDataFileName, getSysconfDir
  ) where

import qualified Control.Exception as Exception
import Data.Version (Version(..))
import System.Environment (getEnv)
import Prelude

catchIO :: IO a -> (Exception.IOException -> IO a) -> IO a
catchIO = Exception.catch


version :: Version
version = Version {versionBranch = [0,8,0], versionTags = []}
bindir, libdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/media/Data/School/CompSci/sproxy/.cabal-sandbox/bin"
libdir     = "/media/Data/School/CompSci/sproxy/.cabal-sandbox/lib/x86_64-linux-ghc-7.8.3/sproxy-0.8.0"
datadir    = "/media/Data/School/CompSci/sproxy/.cabal-sandbox/share/x86_64-linux-ghc-7.8.3/sproxy-0.8.0"
libexecdir = "/media/Data/School/CompSci/sproxy/.cabal-sandbox/libexec"
sysconfdir = "/media/Data/School/CompSci/sproxy/.cabal-sandbox/etc"

getBinDir, getLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "sproxy_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "sproxy_libdir") (\_ -> return libdir)
getDataDir = catchIO (getEnv "sproxy_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "sproxy_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "sproxy_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
