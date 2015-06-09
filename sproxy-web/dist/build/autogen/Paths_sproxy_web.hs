module Paths_sproxy_web (
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
version = Version {versionBranch = [0,2,0,0], versionTags = []}
bindir, libdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/media/Data/School/CompSci/sproxy-web/.cabal-sandbox/bin"
libdir     = "/media/Data/School/CompSci/sproxy-web/.cabal-sandbox/lib/x86_64-linux-ghc-7.8.3/sproxy-web-0.2.0.0"
datadir    = "/media/Data/School/CompSci/sproxy-web/.cabal-sandbox/share/x86_64-linux-ghc-7.8.3/sproxy-web-0.2.0.0"
libexecdir = "/media/Data/School/CompSci/sproxy-web/.cabal-sandbox/libexec"
sysconfdir = "/media/Data/School/CompSci/sproxy-web/.cabal-sandbox/etc"

getBinDir, getLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "sproxy_web_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "sproxy_web_libdir") (\_ -> return libdir)
getDataDir = catchIO (getEnv "sproxy_web_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "sproxy_web_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "sproxy_web_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
