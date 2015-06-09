module Paths_example (
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
version = Version {versionBranch = [0,1,0,0], versionTags = []}
bindir, libdir, datadir, libexecdir, sysconfdir :: FilePath

bindir     = "/media/Data/School/CompSci/sproxy/example/.cabal-sandbox/bin"
libdir     = "/media/Data/School/CompSci/sproxy/example/.cabal-sandbox/lib/x86_64-linux-ghc-7.8.3/example-0.1.0.0"
datadir    = "/media/Data/School/CompSci/sproxy/example/.cabal-sandbox/share/x86_64-linux-ghc-7.8.3/example-0.1.0.0"
libexecdir = "/media/Data/School/CompSci/sproxy/example/.cabal-sandbox/libexec"
sysconfdir = "/media/Data/School/CompSci/sproxy/example/.cabal-sandbox/etc"

getBinDir, getLibDir, getDataDir, getLibexecDir, getSysconfDir :: IO FilePath
getBinDir = catchIO (getEnv "example_bindir") (\_ -> return bindir)
getLibDir = catchIO (getEnv "example_libdir") (\_ -> return libdir)
getDataDir = catchIO (getEnv "example_datadir") (\_ -> return datadir)
getLibexecDir = catchIO (getEnv "example_libexecdir") (\_ -> return libexecdir)
getSysconfDir = catchIO (getEnv "example_sysconfdir") (\_ -> return sysconfdir)

getDataFileName :: FilePath -> IO FilePath
getDataFileName name = do
  dir <- getDataDir
  return (dir ++ "/" ++ name)
