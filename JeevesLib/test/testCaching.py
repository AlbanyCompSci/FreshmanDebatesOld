import unittest
import macropy.activate
from sourcetrans.macro_module import macros, jeeves
import JeevesLib
import operator

@jeeves
class TestClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b

@jeeves
class TestClassMethod:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def add_a_to_b(self):
        self.b += self.a

    def return_sum(self):
        return self.a + self.b

@jeeves
class TestClass1:
    def __init__(self, a):
        self.a = a
    def __getstate__(self):
        if hasattr(self.a, '__getstate__'):
            return "(TestClass1:%s)" % self.a.__getstate__()
        else:
            return "(TestClass1:%s)" % repr(self.a)

@jeeves
class TestClass1Eq:
    def __init__(self, a):
        self.a = a
    def __eq__(self, other):
        return self.a == other.a
    def __ne__(self, other):
        return self.a != other.a
    def __lt__(self, other):
        return self.a < other.a
    def __gt__(self, other):
        return self.a > other.a
    def __le__(self, other):
        return self.a <= other.a
    def __ge__(self, other):
        return self.a >= other.a

class TestSourceTransform(unittest.TestCase):
    def setUp(self):
        # reset the Jeeves state
        JeevesLib.init()
        JeevesLib.start_caching()

    @jeeves
    def test_restrict_all_permissive(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda _: True)
        self.assertTrue(JeevesLib.concretize(None, x))

        # Now we test the cache.
        self.assertTrue(JeevesLib.concretize(None, x))
        self.assertEqual(len(JeevesLib.get_cache()), 1)

    @jeeves
    def test_restrict_all_restrictive(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda _: False)
        self.assertFalse(JeevesLib.concretize(None, x))
        self.assertFalse(JeevesLib.concretize(None, x))

    @jeeves
    def test_restrict_with_context(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda y: y == 2)

        self.assertTrue(JeevesLib.concretize(2, x))
        self.assertTrue(JeevesLib.concretize(2, x))

        self.assertFalse(JeevesLib.concretize(3, x))
        self.assertFalse(JeevesLib.concretize(3, x))

    @jeeves
    def test_restrict_with_sensitive_value(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda y: y == 2)
        value = JeevesLib.mkSensitive(x, 42, 41)

        self.assertEquals(JeevesLib.concretize(2, value), 42)
        self.assertEquals(JeevesLib.concretize(2, value), 42)

        self.assertEquals(JeevesLib.concretize(1, value), 41)
        self.assertEquals(JeevesLib.concretize(1, value), 41)

        self.assertEquals(len(JeevesLib.get_cache()), 2)

    @jeeves
    def test_restrict_with_cyclic(self):
        jl = JeevesLib
        jl.clear_cache()

        # use the value itself as the context
        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt == 42)

        value = jl.mkSensitive(x, 42, 20)
        self.assertEquals(jl.concretize(value, value), 42)
        self.assertEquals(jl.concretize(value, value), 42)

        value = jl.mkSensitive(x, 41, 20)
        self.assertEquals(jl.concretize(value, value), 20)
        self.assertEquals(jl.concretize(value, value), 20)
    
    @jeeves
    def test_restrict_under_conditional(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')

        value = JeevesLib.mkSensitive(x, 42, 0)
        if value == 42:
            JeevesLib.restrict(x, lambda ctxt : ctxt == 1)
        self.assertEquals(JeevesLib.concretize(0, value), 0)
        self.assertEquals(JeevesLib.concretize(0, value), 0)
        self.assertEquals(JeevesLib.concretize(1, value), 42)
        self.assertEquals(JeevesLib.concretize(1, value), 42)

        y = JeevesLib.mkLabel('y')

        value = JeevesLib.mkSensitive(y, 43, 0)
        if value == 42:
            JeevesLib.restrict(y, lambda ctxt : ctxt == 1)
        self.assertEquals(JeevesLib.concretize(0, value), 43)
        self.assertEquals(JeevesLib.concretize(0, value), 43)
        self.assertEquals(JeevesLib.concretize(1, value), 43)
        self.assertEquals(JeevesLib.concretize(1, value), 43)

    @jeeves
    def test_jbool_functions_fexprs(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda (a,_) : a == 42)

        for lh in (True, False):
            for ll in (True, False):
                for rh in (True, False):
                    for rl in (True, False):
                        l = jl.mkSensitive(x, lh, ll)
                        r = jl.mkSensitive(x, rh, rl)
                        self.assertEquals(
                              jl.concretize((42,0), l and r)
                            , operator.and_(lh, rh))
                        self.assertEquals(
                              jl.concretize((42,0), l and r)
                            , operator.and_(lh, rh))
                        self.assertEquals(
                              jl.concretize((10,0), l and r)
                            , operator.and_(ll, rl))
                        self.assertEquals(
                              jl.concretize((10,0), l and r)
                            , operator.and_(ll, rl))
      
    @jeeves
    def test_jif_with_assign(self):
        jl = JeevesLib
        jl.clear_cache()

        y = jl.mkLabel('y')
        jl.restrict(y, lambda ctxt : ctxt == 42)

        value0 = jl.mkSensitive(y, 0, 1)
        value2 = jl.mkSensitive(y, 2, 3)

        value = value0
        value = value2
        self.assertEquals(jl.concretize(42, value), 2)
        self.assertEquals(jl.concretize(10, value), 3)
        self.assertEquals(jl.concretize(42, value), 2)
        self.assertEquals(jl.concretize(10, value), 3)

        value = 100
        value = value2
        self.assertEquals(jl.concretize(42, value), 2)
        self.assertEquals(jl.concretize(10, value), 3)
        self.assertEquals(jl.concretize(42, value), 2)
        self.assertEquals(jl.concretize(10, value), 3)

        value = value0
        value = 200
        self.assertEquals(jl.concretize(42, value), 200)
        self.assertEquals(jl.concretize(10, value), 200)
        self.assertEquals(jl.concretize(42, value), 200)
        self.assertEquals(jl.concretize(10, value), 200)

        value = 100
        value = 200
        self.assertEquals(jl.concretize(42, value), 200)
        self.assertEquals(jl.concretize(10, value), 200)
        self.assertEquals(jl.concretize(42, value), 200)
        self.assertEquals(jl.concretize(10, value), 200)

    @jeeves
    def test_jif_with_assign_with_pathvars(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        y = jl.mkLabel('y')
        jl.restrict(x, lambda (a,_) : a)
        jl.restrict(y, lambda (_,b) : b)

        value0 = jl.mkSensitive(y, 0, 1)
        value2 = jl.mkSensitive(y, 2, 3)

        value = value0
        if x:
            value = value2
        self.assertEquals(jl.concretize((True, True), value), 2)
        self.assertEquals(jl.concretize((True, False), value), 3)
        self.assertEquals(jl.concretize((False, True), value), 0)
        self.assertEquals(jl.concretize((False, False), value), 1)
        self.assertEquals(jl.concretize((True, True), value), 2)
        self.assertEquals(jl.concretize((True, False), value), 3)
        self.assertEquals(jl.concretize((False, True), value), 0)
        self.assertEquals(jl.concretize((False, False), value), 1)

        value = value0
        if not x:
            value = value2
        self.assertEquals(jl.concretize((False, True), value), 2)
        self.assertEquals(jl.concretize((False, False), value), 3)
        self.assertEquals(jl.concretize((True, True), value), 0)
        self.assertEquals(jl.concretize((True, False), value), 1)
        self.assertEquals(jl.concretize((False, True), value), 2)
        self.assertEquals(jl.concretize((False, False), value), 3)
        self.assertEquals(jl.concretize((True, True), value), 0)
        self.assertEquals(jl.concretize((True, False), value), 1)

    @jeeves
    def test_function_facets(self):
        def add1(a):
            return a+1
        def add2(a):
            return a+2

        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt == 42)

        fun = jl.mkSensitive(x, add1, add2)
        value = fun(15)
        self.assertEquals(jl.concretize(42, value), 16)
        self.assertEquals(jl.concretize(41, value), 17)
        self.assertEquals(jl.concretize(42, value), 16)
        self.assertEquals(jl.concretize(41, value), 17)

    @jeeves
    def test_objects_faceted(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt)

        y = jl.mkSensitive(x,
            TestClass(1, 2),
            TestClass(3, 4))

        self.assertEquals(jl.concretize(True, y.a), 1)
        self.assertEquals(jl.concretize(True, y.b), 2)
        self.assertEquals(jl.concretize(False, y.a), 3)
        self.assertEquals(jl.concretize(False, y.b), 4)
        self.assertEquals(jl.concretize(True, y.a), 1)
        self.assertEquals(jl.concretize(True, y.b), 2)
        self.assertEquals(jl.concretize(False, y.a), 3)
        self.assertEquals(jl.concretize(False, y.b), 4)

    @jeeves
    def test_objects_mutate(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt)

        s = TestClass(1, None)
        t = TestClass(3, None)
        y = jl.mkSensitive(x, s, t)

        if y.a == 1:
            y.a = y.a + 100

        self.assertEquals(jl.concretize(True, y.a), 101)
        self.assertEquals(jl.concretize(True, s.a), 101)
        self.assertEquals(jl.concretize(True, t.a), 3)
        self.assertEquals(jl.concretize(False, y.a), 3)
        self.assertEquals(jl.concretize(False, s.a), 1)
        self.assertEquals(jl.concretize(False, t.a), 3)
        self.assertEquals(jl.concretize(True, y.a), 101)
        self.assertEquals(jl.concretize(True, s.a), 101)
        self.assertEquals(jl.concretize(True, t.a), 3)
        self.assertEquals(jl.concretize(False, y.a), 3)
        self.assertEquals(jl.concretize(False, s.a), 1)
        self.assertEquals(jl.concretize(False, t.a), 3)

    @jeeves
    def test_context_mutate(self):
        jl = JeevesLib
        jl.clear_cache()

        test_alice = TestClass(1, 1)
        test_bob = TestClass(2, 2)

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt: ctxt.a == 1)

        y = jl.mkSensitive(x, 42, 0)

        self.assertEquals(jl.concretize(test_alice, y), 42)
        self.assertEquals(jl.concretize(test_bob, y), 0)

        test_alice.a = 2
        test_bob.a = 1
        self.assertEquals(jl.concretize(test_alice, y), 0)
        self.assertEquals(jl.concretize(test_bob, y), 42)

    @jeeves
    def test_objects_methodcall(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt)

        s = TestClassMethod(1, 10)
        t = TestClassMethod(100, 1000)
        y = jl.mkSensitive(x, s, t)

        self.assertEquals(jl.concretize(True, y.return_sum()), 11)
        self.assertEquals(jl.concretize(False, y.return_sum()), 1100)
        self.assertEquals(jl.concretize(True, y.return_sum()), 11)
        self.assertEquals(jl.concretize(False, y.return_sum()), 1100)

        y.add_a_to_b()
        self.assertEquals(jl.concretize(True, s.a), 1)
        self.assertEquals(jl.concretize(True, s.b), 11)
        self.assertEquals(jl.concretize(True, t.a), 100)
        self.assertEquals(jl.concretize(True, t.b), 1000)
        self.assertEquals(jl.concretize(True, y.a), 1)
        self.assertEquals(jl.concretize(True, y.b), 11)
        self.assertEquals(jl.concretize(False, s.a), 1)
        self.assertEquals(jl.concretize(False, s.b), 10)
        self.assertEquals(jl.concretize(False, t.a), 100)
        self.assertEquals(jl.concretize(False, t.b), 1100)
        self.assertEquals(jl.concretize(False, y.a), 100)
        self.assertEquals(jl.concretize(False, y.b), 1100)
        self.assertEquals(jl.concretize(True, s.a), 1)
        self.assertEquals(jl.concretize(True, s.b), 11)
        self.assertEquals(jl.concretize(True, t.a), 100)
        self.assertEquals(jl.concretize(True, t.b), 1000)
        self.assertEquals(jl.concretize(True, y.a), 1)
        self.assertEquals(jl.concretize(True, y.b), 11)
        self.assertEquals(jl.concretize(False, s.a), 1)
        self.assertEquals(jl.concretize(False, s.b), 10)
        self.assertEquals(jl.concretize(False, t.a), 100)
        self.assertEquals(jl.concretize(False, t.b), 1100)
        self.assertEquals(jl.concretize(False, y.a), 100)
        self.assertEquals(jl.concretize(False, y.b), 1100)
 
    @jeeves
    def test_objects_eq_is(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt)

        a = TestClass1(3)
        b = TestClass1(3)
        c = TestClass1(2)

        # Ensure that a < b and b < c (will probably be true anyway,
        # just making sure)
        s = sorted((a, b, c))
        a = s[0]
        b = s[1]
        c = s[2]
        a.a = 3
        b.a = 3
        c.a = 2

        v1 = jl.mkSensitive(x, a, c)
        v2 = jl.mkSensitive(x, b, c)
        v3 = jl.mkSensitive(x, c, a)
    
        self.assertEquals(jl.concretize(True, v1 == v1), True)
        self.assertEquals(jl.concretize(True, v2 == v2), True)
        self.assertEquals(jl.concretize(True, v3 == v3), True)
        self.assertEquals(jl.concretize(True, v1 == v2), False)
        self.assertEquals(jl.concretize(True, v2 == v3), False)
        self.assertEquals(jl.concretize(True, v3 == v1), False)
        self.assertEquals(jl.concretize(True, v1 == v1), True)
        self.assertEquals(jl.concretize(True, v2 == v2), True)
        self.assertEquals(jl.concretize(True, v3 == v3), True)
        self.assertEquals(jl.concretize(True, v1 == v2), False)
        self.assertEquals(jl.concretize(True, v2 == v3), False)
        self.assertEquals(jl.concretize(True, v3 == v1), False)

        self.assertEquals(jl.concretize(True, v1 != v1), False)
        self.assertEquals(jl.concretize(True, v2 != v2), False)
        self.assertEquals(jl.concretize(True, v3 != v3), False)
        self.assertEquals(jl.concretize(True, v1 != v2), True)
        self.assertEquals(jl.concretize(True, v2 != v3), True)
        self.assertEquals(jl.concretize(True, v3 != v1), True)
        self.assertEquals(jl.concretize(True, v1 != v1), False)
        self.assertEquals(jl.concretize(True, v2 != v2), False)
        self.assertEquals(jl.concretize(True, v3 != v3), False)
        self.assertEquals(jl.concretize(True, v1 != v2), True)
        self.assertEquals(jl.concretize(True, v2 != v3), True)
        self.assertEquals(jl.concretize(True, v3 != v1), True)

        self.assertEquals(jl.concretize(True, v1 < v1), False)
        self.assertEquals(jl.concretize(True, v2 < v2), False)
        self.assertEquals(jl.concretize(True, v3 < v3), False)
        self.assertEquals(jl.concretize(True, v1 < v2), True)
        self.assertEquals(jl.concretize(True, v2 < v3), True)
        self.assertEquals(jl.concretize(True, v3 < v1), False)
        self.assertEquals(jl.concretize(True, v1 < v1), False)
        self.assertEquals(jl.concretize(True, v2 < v2), False)
        self.assertEquals(jl.concretize(True, v3 < v3), False)
        self.assertEquals(jl.concretize(True, v1 < v2), True)
        self.assertEquals(jl.concretize(True, v2 < v3), True)
        self.assertEquals(jl.concretize(True, v3 < v1), False)

        self.assertEquals(jl.concretize(True, v1 > v1), False)
        self.assertEquals(jl.concretize(True, v2 > v2), False)
        self.assertEquals(jl.concretize(True, v3 > v3), False)
        self.assertEquals(jl.concretize(True, v1 > v2), False)
        self.assertEquals(jl.concretize(True, v2 > v3), False)
        self.assertEquals(jl.concretize(True, v3 > v1), True)
        self.assertEquals(jl.concretize(True, v1 > v1), False)
        self.assertEquals(jl.concretize(True, v2 > v2), False)
        self.assertEquals(jl.concretize(True, v3 > v3), False)
        self.assertEquals(jl.concretize(True, v1 > v2), False)
        self.assertEquals(jl.concretize(True, v2 > v3), False)
        self.assertEquals(jl.concretize(True, v3 > v1), True)

        self.assertEquals(jl.concretize(True, v1 <= v1), True)
        self.assertEquals(jl.concretize(True, v2 <= v2), True)
        self.assertEquals(jl.concretize(True, v3 <= v3), True)
        self.assertEquals(jl.concretize(True, v1 <= v2), True)
        self.assertEquals(jl.concretize(True, v2 <= v3), True)
        self.assertEquals(jl.concretize(True, v3 <= v1), False)
        self.assertEquals(jl.concretize(True, v1 <= v1), True)
        self.assertEquals(jl.concretize(True, v2 <= v2), True)
        self.assertEquals(jl.concretize(True, v3 <= v3), True)
        self.assertEquals(jl.concretize(True, v1 <= v2), True)
        self.assertEquals(jl.concretize(True, v2 <= v3), True)
        self.assertEquals(jl.concretize(True, v3 <= v1), False)

        self.assertEquals(jl.concretize(True, v1 >= v1), True)
        self.assertEquals(jl.concretize(True, v2 >= v2), True)
        self.assertEquals(jl.concretize(True, v3 >= v3), True)
        self.assertEquals(jl.concretize(True, v1 >= v2), False)
        self.assertEquals(jl.concretize(True, v2 >= v3), False)
        self.assertEquals(jl.concretize(True, v3 >= v1), True)
        self.assertEquals(jl.concretize(True, v1 >= v1), True)
        self.assertEquals(jl.concretize(True, v2 >= v2), True)
        self.assertEquals(jl.concretize(True, v3 >= v3), True)
        self.assertEquals(jl.concretize(True, v1 >= v2), False)
        self.assertEquals(jl.concretize(True, v2 >= v3), False)
        self.assertEquals(jl.concretize(True, v3 >= v1), True)

        self.assertEquals(jl.concretize(False, v2 == v3), False)
        self.assertEquals(jl.concretize(False, v2 != v3), True)
        self.assertEquals(jl.concretize(False, v2 < v3), False)
        self.assertEquals(jl.concretize(False, v2 > v3), True)
        self.assertEquals(jl.concretize(False, v2 <= v3), False)
        self.assertEquals(jl.concretize(False, v2 >= v3), True)
        self.assertEquals(jl.concretize(False, v2 == v3), False)
        self.assertEquals(jl.concretize(False, v2 != v3), True)
        self.assertEquals(jl.concretize(False, v2 < v3), False)
        self.assertEquals(jl.concretize(False, v2 > v3), True)
        self.assertEquals(jl.concretize(False, v2 <= v3), False)
        self.assertEquals(jl.concretize(False, v2 >= v3), True)

        a = TestClass1Eq(3)
        b = TestClass1Eq(3)
        c = TestClass1Eq(2)

        v1 = jl.mkSensitive(x, a, c)
        v2 = jl.mkSensitive(x, b, c)
        v3 = jl.mkSensitive(x, c, a)
    
        self.assertEquals(jl.concretize(True, v1 == v1), True)
        self.assertEquals(jl.concretize(True, v2 == v2), True)
        self.assertEquals(jl.concretize(True, v3 == v3), True)
        self.assertEquals(jl.concretize(True, v1 == v2), True)
        self.assertEquals(jl.concretize(True, v2 == v3), False)
        self.assertEquals(jl.concretize(True, v3 == v1), False)
        self.assertEquals(jl.concretize(True, v1 == v1), True)
        self.assertEquals(jl.concretize(True, v2 == v2), True)
        self.assertEquals(jl.concretize(True, v3 == v3), True)
        self.assertEquals(jl.concretize(True, v1 == v2), True)
        self.assertEquals(jl.concretize(True, v2 == v3), False)
        self.assertEquals(jl.concretize(True, v3 == v1), False)

        self.assertEquals(jl.concretize(True, v1 != v1), False)
        self.assertEquals(jl.concretize(True, v2 != v2), False)
        self.assertEquals(jl.concretize(True, v3 != v3), False)
        self.assertEquals(jl.concretize(True, v1 != v2), False)
        self.assertEquals(jl.concretize(True, v2 != v3), True)
        self.assertEquals(jl.concretize(True, v3 != v1), True)
        self.assertEquals(jl.concretize(True, v1 != v1), False)
        self.assertEquals(jl.concretize(True, v2 != v2), False)
        self.assertEquals(jl.concretize(True, v3 != v3), False)
        self.assertEquals(jl.concretize(True, v1 != v2), False)
        self.assertEquals(jl.concretize(True, v2 != v3), True)
        self.assertEquals(jl.concretize(True, v3 != v1), True)

        self.assertEquals(jl.concretize(True, v1 < v1), False)
        self.assertEquals(jl.concretize(True, v2 < v2), False)
        self.assertEquals(jl.concretize(True, v3 < v3), False)
        self.assertEquals(jl.concretize(True, v1 < v2), False)
        self.assertEquals(jl.concretize(True, v2 < v3), False)
        self.assertEquals(jl.concretize(True, v3 < v1), True)
        self.assertEquals(jl.concretize(True, v1 < v1), False)
        self.assertEquals(jl.concretize(True, v2 < v2), False)
        self.assertEquals(jl.concretize(True, v3 < v3), False)
        self.assertEquals(jl.concretize(True, v1 < v2), False)
        self.assertEquals(jl.concretize(True, v2 < v3), False)
        self.assertEquals(jl.concretize(True, v3 < v1), True)

        self.assertEquals(jl.concretize(True, v1 > v1), False)
        self.assertEquals(jl.concretize(True, v2 > v2), False)
        self.assertEquals(jl.concretize(True, v3 > v3), False)
        self.assertEquals(jl.concretize(True, v1 > v2), False)
        self.assertEquals(jl.concretize(True, v2 > v3), True)
        self.assertEquals(jl.concretize(True, v3 > v1), False)
        self.assertEquals(jl.concretize(True, v1 > v1), False)
        self.assertEquals(jl.concretize(True, v2 > v2), False)
        self.assertEquals(jl.concretize(True, v3 > v3), False)
        self.assertEquals(jl.concretize(True, v1 > v2), False)
        self.assertEquals(jl.concretize(True, v2 > v3), True)
        self.assertEquals(jl.concretize(True, v3 > v1), False)

        self.assertEquals(jl.concretize(True, v1 <= v1), True)
        self.assertEquals(jl.concretize(True, v2 <= v2), True)
        self.assertEquals(jl.concretize(True, v3 <= v3), True)
        self.assertEquals(jl.concretize(True, v1 <= v2), True)
        self.assertEquals(jl.concretize(True, v2 <= v3), False)
        self.assertEquals(jl.concretize(True, v3 <= v1), True)
        self.assertEquals(jl.concretize(True, v1 <= v1), True)
        self.assertEquals(jl.concretize(True, v2 <= v2), True)
        self.assertEquals(jl.concretize(True, v3 <= v3), True)
        self.assertEquals(jl.concretize(True, v1 <= v2), True)
        self.assertEquals(jl.concretize(True, v2 <= v3), False)
        self.assertEquals(jl.concretize(True, v3 <= v1), True)

        self.assertEquals(jl.concretize(True, v1 >= v1), True)
        self.assertEquals(jl.concretize(True, v2 >= v2), True)
        self.assertEquals(jl.concretize(True, v3 >= v3), True)
        self.assertEquals(jl.concretize(True, v1 >= v2), True)
        self.assertEquals(jl.concretize(True, v2 >= v3), True)
        self.assertEquals(jl.concretize(True, v3 >= v1), False)
        self.assertEquals(jl.concretize(True, v1 >= v1), True)
        self.assertEquals(jl.concretize(True, v2 >= v2), True)
        self.assertEquals(jl.concretize(True, v3 >= v3), True)
        self.assertEquals(jl.concretize(True, v1 >= v2), True)
        self.assertEquals(jl.concretize(True, v2 >= v3), True)
        self.assertEquals(jl.concretize(True, v3 >= v1), False)

        self.assertEquals(jl.concretize(False, v2 == v3), False)
        self.assertEquals(jl.concretize(False, v2 != v3), True)
        self.assertEquals(jl.concretize(False, v2 < v3), True)
        self.assertEquals(jl.concretize(False, v2 > v3), False)
        self.assertEquals(jl.concretize(False, v2 <= v3), True)
        self.assertEquals(jl.concretize(False, v2 >= v3), False)
        self.assertEquals(jl.concretize(False, v2 == v3), False)
        self.assertEquals(jl.concretize(False, v2 != v3), True)
        self.assertEquals(jl.concretize(False, v2 < v3), True)
        self.assertEquals(jl.concretize(False, v2 > v3), False)
        self.assertEquals(jl.concretize(False, v2 <= v3), True)
        self.assertEquals(jl.concretize(False, v2 >= v3), False)

    @jeeves
    def test_jhasElt(self):
        jl = JeevesLib
        jl.clear_cache()

        a = jl.mkLabel ()
        jl.restrict(a, lambda x: x)
        xS = jl.mkSensitive(a, 42, 1)

        b = jl.mkLabel ()
        jl.restrict(b, lambda x: x)
        yS = jl.mkSensitive(b, 43, 3)

        lst = [xS, 2, yS]
        self.assertEquals(jl.concretize(True, 42 in lst) , True)
        self.assertEquals(jl.concretize(False, 42 in lst) , False)
        self.assertEquals(jl.concretize(True, 1 in lst) , False)
        self.assertEquals(jl.concretize(False, 1 in lst) , True)
        self.assertEquals(jl.concretize(True, 43 in lst) , True)
        self.assertEquals(jl.concretize(False, 43 in lst) , False)
        self.assertEquals(jl.concretize(True, 3 in lst) , False)
        self.assertEquals(jl.concretize(False, 3 in lst) , True)
        self.assertEquals(jl.concretize(True, 42 in lst) , True)
        self.assertEquals(jl.concretize(False, 42 in lst) , False)
        self.assertEquals(jl.concretize(True, 1 in lst) , False)
        self.assertEquals(jl.concretize(False, 1 in lst) , True)
        self.assertEquals(jl.concretize(True, 43 in lst) , True)
        self.assertEquals(jl.concretize(False, 43 in lst) , False)
        self.assertEquals(jl.concretize(True, 3 in lst) , False)
        self.assertEquals(jl.concretize(False, 3 in lst) , True)

    @jeeves
    def test_list(self):
        jl = JeevesLib
        jl.clear_cache()

        x = jl.mkLabel('x')
        jl.restrict(x, lambda ctxt : ctxt)

        l = jl.mkSensitive(x, [40,41,42], [0,1,2,3])

        self.assertEqual(jl.concretize(True, l[0]), 40)
        self.assertEqual(jl.concretize(True, l[1]), 41)
        self.assertEqual(jl.concretize(True, l[2]), 42)
        self.assertEqual(jl.concretize(False, l[0]), 0)
        self.assertEqual(jl.concretize(False, l[1]), 1)
        self.assertEqual(jl.concretize(False, l[2]), 2)
        self.assertEqual(jl.concretize(False, l[3]), 3)
        self.assertEqual(jl.concretize(True, l[0]), 40)
        self.assertEqual(jl.concretize(True, l[1]), 41)
        self.assertEqual(jl.concretize(True, l[2]), 42)
        self.assertEqual(jl.concretize(False, l[0]), 0)
        self.assertEqual(jl.concretize(False, l[1]), 1)
        self.assertEqual(jl.concretize(False, l[2]), 2)
        self.assertEqual(jl.concretize(False, l[3]), 3)

        self.assertEqual(jl.concretize(True, l.__len__()), 3)
        self.assertEqual(jl.concretize(False, l.__len__()), 4)
        self.assertEqual(jl.concretize(True, l.__len__()), 3)
        self.assertEqual(jl.concretize(False, l.__len__()), 4)

        l[1] = 19

        self.assertEqual(jl.concretize(True, l[0]), 40)
        self.assertEqual(jl.concretize(True, l[1]), 19)
        self.assertEqual(jl.concretize(True, l[2]), 42)
        self.assertEqual(jl.concretize(False, l[0]), 0)
        self.assertEqual(jl.concretize(False, l[1]), 19)
        self.assertEqual(jl.concretize(False, l[2]), 2)
        self.assertEqual(jl.concretize(False, l[3]), 3)
        self.assertEqual(jl.concretize(True, l[0]), 40)
        self.assertEqual(jl.concretize(True, l[1]), 19)
        self.assertEqual(jl.concretize(True, l[2]), 42)
        self.assertEqual(jl.concretize(False, l[0]), 0)
        self.assertEqual(jl.concretize(False, l[1]), 19)
        self.assertEqual(jl.concretize(False, l[2]), 2)
        self.assertEqual(jl.concretize(False, l[3]), 3)

    @jeeves
    def test_jmap(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda ctxt : ctxt)

        l = JeevesLib.mkSensitive(x, [0,1,2], [3,4,5,6])
        m = [x*x for x in l]

        self.assertEqual(JeevesLib.concretize(True, m[0]), 0)
        self.assertEqual(JeevesLib.concretize(True, m[1]), 1)
        self.assertEqual(JeevesLib.concretize(True, m[2]), 4)
        self.assertEqual(JeevesLib.concretize(False, m[0]), 9)
        self.assertEqual(JeevesLib.concretize(False, m[1]), 16)
        self.assertEqual(JeevesLib.concretize(False, m[2]), 25)
        self.assertEqual(JeevesLib.concretize(False, m[3]), 36)
        self.assertEqual(JeevesLib.concretize(True, m[0]), 0)
        self.assertEqual(JeevesLib.concretize(True, m[1]), 1)
        self.assertEqual(JeevesLib.concretize(True, m[2]), 4)
        self.assertEqual(JeevesLib.concretize(False, m[0]), 9)
        self.assertEqual(JeevesLib.concretize(False, m[1]), 16)
        self.assertEqual(JeevesLib.concretize(False, m[2]), 25)
        self.assertEqual(JeevesLib.concretize(False, m[3]), 36)
    
    @jeeves
    def test_jmap_for(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda ctxt : ctxt)

        l = JeevesLib.mkSensitive(x, [0,1,2], [3,4,5,6])
        m = 0
        for t in l:
            m = m + t*t

        self.assertEqual(JeevesLib.concretize(True, m), 5)
        self.assertEqual(JeevesLib.concretize(False, m), 86)
        self.assertEqual(JeevesLib.concretize(True, m), 5)
        self.assertEqual(JeevesLib.concretize(False, m), 86)

    @jeeves
    def test_jlist(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda ctxt : ctxt)

        l = JeevesLib.mkSensitive(x, [0,1,2], [3,4,5,6])
        if x:
            l.append(10)
        else:
            l.append(11)

        self.assertEqual(JeevesLib.concretize(True, l[0]), 0)
        self.assertEqual(JeevesLib.concretize(True, l[1]), 1)
        self.assertEqual(JeevesLib.concretize(True, l[2]), 2)
        self.assertEqual(JeevesLib.concretize(True, l[3]), 10)
        self.assertEqual(JeevesLib.concretize(False, l[0]), 3)
        self.assertEqual(JeevesLib.concretize(False, l[1]), 4)
        self.assertEqual(JeevesLib.concretize(False, l[2]), 5)
        self.assertEqual(JeevesLib.concretize(False, l[3]), 6)
        self.assertEqual(JeevesLib.concretize(False, l[4]), 11)
        self.assertEqual(JeevesLib.concretize(True, l[0]), 0)
        self.assertEqual(JeevesLib.concretize(True, l[1]), 1)
        self.assertEqual(JeevesLib.concretize(True, l[2]), 2)
        self.assertEqual(JeevesLib.concretize(True, l[3]), 10)
        self.assertEqual(JeevesLib.concretize(False, l[0]), 3)
        self.assertEqual(JeevesLib.concretize(False, l[1]), 4)
        self.assertEqual(JeevesLib.concretize(False, l[2]), 5)
        self.assertEqual(JeevesLib.concretize(False, l[3]), 6)
        self.assertEqual(JeevesLib.concretize(False, l[4]), 11)

        if x:
            l[0] = 20
        self.assertEqual(JeevesLib.concretize(True, l[0]), 20)
        self.assertEqual(JeevesLib.concretize(False, l[0]), 3)
        self.assertEqual(JeevesLib.concretize(True, l[0]), 20)
        self.assertEqual(JeevesLib.concretize(False, l[0]), 3)

    @jeeves
    def test_scope(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda ctxt : ctxt)

        y = 5

        def awesome_function():
            y = 7
            if x:
                return 30
            y = 19
            return 17

        z = awesome_function()

        self.assertEqual(JeevesLib.concretize(True, y), 5)
        self.assertEqual(JeevesLib.concretize(False, y), 5)
        self.assertEqual(JeevesLib.concretize(True, z), 30)
        self.assertEqual(JeevesLib.concretize(False, z), 17)
        self.assertEqual(JeevesLib.concretize(True, y), 5)
        self.assertEqual(JeevesLib.concretize(False, y), 5)
        self.assertEqual(JeevesLib.concretize(True, z), 30)
        self.assertEqual(JeevesLib.concretize(False, z), 17)

    @jeeves
    def test_jfun(self):
        JeevesLib.clear_cache()

        x = JeevesLib.mkLabel('x')
        JeevesLib.restrict(x, lambda ctxt : ctxt)
 
        y = JeevesLib.mkSensitive(x, [1,2,3], [4,5,6,7])

        z = [x*x for x in y]

        self.assertEqual(JeevesLib.concretize(True, z[0]), 1)
        self.assertEqual(JeevesLib.concretize(True, z[1]), 4)
        self.assertEqual(JeevesLib.concretize(True, z[2]), 9)
        self.assertEqual(JeevesLib.concretize(False, z[0]), 16)
        self.assertEqual(JeevesLib.concretize(False, z[1]), 25)
        self.assertEqual(JeevesLib.concretize(False, z[2]), 36)
        self.assertEqual(JeevesLib.concretize(False, z[3]), 49)
        self.assertEqual(JeevesLib.concretize(True, z[0]), 1)
        self.assertEqual(JeevesLib.concretize(True, z[1]), 4)
        self.assertEqual(JeevesLib.concretize(True, z[2]), 9)
        self.assertEqual(JeevesLib.concretize(False, z[0]), 16)
        self.assertEqual(JeevesLib.concretize(False, z[1]), 25)
        self.assertEqual(JeevesLib.concretize(False, z[2]), 36)
        self.assertEqual(JeevesLib.concretize(False, z[3]), 49)
