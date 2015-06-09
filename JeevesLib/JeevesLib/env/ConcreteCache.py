"""Concretization cache.

  :synopsis: This stores the concretized values that have been cached.

  The current strategy is to only cache per page.

  .. moduleauthor:: Jean Yang <jeanyang@csail.mit.edu>

"""
import JeevesLib
import pickle

class ConcreteCache(object):
    """The concrete cache.
    """
    def __init__(self):
        self._cache = {}
        self._should_cache = False

    # Variables that determine whether caching should occur or not.
    def start_caching(self):
        """Turns on caching.
        """
        self._should_cache = True
    def stop_caching(self):
        """Turns off caching.
        """
        self._should_cache = False
    def cache_size(self):
        """Returns the size of the cache.
        """
        return len(self.cache)

    def get_cache_key(self, ctxt, val, pathvars):
        """Makes a cache key string by hashing the state of the context, value,
        and path variables involved in the concretization.

        :param ctxt: Output channel (viewer).
        :type ctxt: T, where policies have type T -> bool
        :param val: Value to concretize.
        :type v: FExpr
        :param pathvars: Path variables involved in the concretization.
        :type pathvars: PathVars
        :returns: The concrete (non-faceted) version of T under the policies
        in the environment.
        """
        if self._should_cache:
            return str(hash(pickle.dumps(ctxt))) + "__" + \
                str(hash(pickle.dumps(val))) + "__" + \
                str(hash(pickle.dumps(pathvars)))
        else:
            return ""

    def cache_value(self, cache_key, cache_value):
        """Caches the value if caching is turned on.

        :param cache_key: Caching key.
        :type cache_key: String.
        :returns: Whether caching occurred.
        """
        if self._should_cache:
            self._cache[cache_key] = cache_value
            return True
        else:
            return False
    def cache_lookup(self, cache_key):
        """Looks up the value in the cache.
        
        :param cache_key: Caching key.
        :type cache_key: String.
        :returns: The concrete (non-faceted) version of T under the policies
        in the environment.
        """
        if self._should_cache:
            try:
                return self._cache[cache_key]
            except KeyError:
                return None
        return None

    def clear_cache(self):
        """Clears the cache of concrete values.
        """
        self._cache = {}
    
    @property
    def cache(self):
        return self._cache
