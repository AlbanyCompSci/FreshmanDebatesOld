Jeeves 1.0
======
Jeeves is a programming language for automatically enforcing privacy policies. We have implemented it as an embedded domain-specific language in Python.

Jeeves helps programmers enforce _information flow policies_ describing where values may flow through a program.
An information flow policy can talk about not just whether Alice can see a sensitive value, but whether Alice can see a value computed from a sensitive value. For instance, a Jeeves policy may describe who can see a user's location in a social network. This policy is enforced not just when a viewer tries to access the location directly, but also when the viewer accesses values computed from the location, for instance the result of a search over all locations. Jeeves policies talk about whether a viewer may see a value. Policies are functions that take an argument corresponding to the output channel and produce a Boolean result.

Jeeves makes it easier for the programmer to enforce privacy policies by making the runtime responsible for producing the appropriate outputs. Jeeves has a _policy-agnostic programming model_: the programmer implements information flow policies separately from the other functionality. The runtime system becomes responsible for enforcing the policies. To allow for policy-agnostic programming, Jeeves asks the programmer to provide multiple views of sensitive values: a _high-confidentiality value_ corresponding to the secret view and a _low-confidentiality value_ corresponding to the public view. For instance, the high-confidentiality view of a user location could be the GPS location and the low-confidentiality view could be the corresponding country. The programmer provides policies about when the high-confidentiality view may be shown. The runtime then executes simultaneously on both views, yielding results that are appropriately guarded by policies. The Jeeves runtime guarantees that a value may only flow to a viewer if the policies allow.

This separation of policy and core functionality relieves programmer burden in keeping track of which policies need to be enforced where. The programmer can separately update policy and core functionality and rely on the runtime to handle the interaction of policies with each other and with the program.

Go ahead, try it out! Feel free to write to the [Jeeves user group](https://groups.google.com/forum/#!forum/jeeves-programmers) with questions.

## Installing Jeeves.
First, you will need Python.

    $ python --version
    Python 2.7.6


### Python libraries
For core Jeeves, we use [MacroPy](https://github.com/lihaoyi/macropy), [Nose](https://nose.readthedocs.org/en/latest/), Django, and [Mock](http://www.voidspace.org.uk/python/mock/). You can install with ```pip``` as follows:

    $ pip install macropy nose django mock
    
For logging in our web demos, we also use Django timelog:

    $ pip install django-timelog


### Other
We also use the [Z3 SMT Solver](http://z3.codeplex.com/releases) for helping resolve label values. Installing the Z3 binaries for your platform *should* install the Python Z3 package. You can test that it works by opening a Python interpreter:

    >>> from z3 import *
    >>> solve(x > 2, y < 10, x + 2*y == 7)
    [y = 0, x = 7]
    >>> print simplify(x + y + 2*x + 3)
    3 + 3*x + y

You may need to build from source so that our code can use the Python Z3 library for interfacing with Z3.

On OSX, if you're familiar with [Homebrew](http://brew.sh/), this is easy:

    $ brew tap homebrew/science
    $ brew install z3

You can also build manually or use nightly build package for OSX(64bit).


## Running Tests.
Once you have installed everything, you should run the tests to make sure everything is working together. To use ```nose```, first make sure your ```PYTHONPATH``` environment variable is set to your current working directory. Then you can run the tests:


    $ cd /to/jeeves
    $ export PYTHONPATH=.
    $ nosetests
    
You can also use ```nose``` to run specific tests. For instance:

    nosetests tests/gallery/authentication

    
## Using Jeeves
There is documentation for the JeevesLib API [here](http://projects.csail.mit.edu/jeeves/doc/jeeveslib.html). There is more documentation on our [Wiki](https://github.com/jeanqasaur/jeeves/wiki). We have a [Quick Introduction to Jeeves](https://github.com/jeanqasaur/jeeves/wiki/A-Quick-Introduction-to-Jeeves). (Happy to take suggestions on how to make it more useful!)

You may also find it helpful to read our tests in ```test``` and ```test/gallery```.
