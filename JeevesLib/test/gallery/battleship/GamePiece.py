from abc import ABCMeta, abstractmethod
from sourcetrans.macro_module import macros, jeeves
import JeevesLib
from fast.ProtectedRef import ProtectedRef, UpdateResult
from util.Singleton import Singleton
from Point import Point

@jeeves
class GamePiece:
  __metaclass__ = ABCMeta

  def __init__(self, owner):
    self.owner = owner  
    self._placedRef = ProtectedRef(False
      , lambda hasShip: lambda ic: (not hasShip) and self.isOwner(ic)
      , None)
    # TODO: See if we can do away with this...
    self._placed = False
    self._bombed = False

    self._squares = []

  def __eq__(self, other):
    return (self.name == other.name and self.owner == other.owner)

  def isOwner(self, ctxt):
    return ctxt.user == self.owner

  # If the current user is allowed to place the pice, then we mark the current
  # piece as placed and return True. Otherwise we return False.
  def placePiece(self, ctxt):
    if (self._placedRef.update(ctxt, ctxt, True) == UpdateResult.Success):
      self._placed = True
      return True
    else:
      return False
  # This is always a concrete value.
  def isPlaced(self):
    return self._placed
  # If the current user is allowed to bomb the piece, then we mark the piece
  # and return True. Otherwise we return False.
  def bombPiece(self, ctxt):
    self._bombed = True;
    return True
  
  # This is always a concrete value.
  def isBombed(self):
    return self._bombed

  # Gets the board coordinates associated with a given piece.
  def getPiecePoints(self, start, end):
    if start.inLine(end) and start.distance(end) == self.size:
      # If we are on the same horizontal line...
      if start.x == end.x:
        yPts = range(start.y
                      , end.y) if start.y < end.y else range(end.y, start.y)
        return map(lambda yPt: Point(start.x, yPt), yPts)
      else:
        xPts = range(start.x
                      , end.x) if start.x < end.x else range(end.x, start.x)
        return map(lambda xPt: Point(xPt, start.y), xPts)
    else:
      return None
  
  # Adds a piece to the list of squares associated with a given piece.
  def addSquare(self, s):
    self._squares.append(s)
    return True
  def getSquares(self):
    return self._squares

class Carrier(GamePiece):
  name = 'carrier'
  def __init__(self, owner):
    self.size = 5
    GamePiece.__init__(self, owner)
class Battleship(GamePiece):
  name = 'battleship'
  def __init__(self, owner):
    self.size = 4
    GamePiece.__init__(self, owner)
class Cruiser(GamePiece):
  name = 'cruiser'
  def __init__(self, owner):
    self.size = 3
    GamePiece.__init__(self, owner)
class Destroyer(GamePiece):
  name = 'destroyer'
  def __init__(self, owner):
    self.size = 2
    GamePiece.__init__(self, owner)
class Submarine(GamePiece):
  name = 'submarine'
  def __init__(self, owner):
    self.size = 1
    GamePiece.__init__(self, owner)
class NoShip(GamePiece, Singleton):
  name = 'noship'
  def __init__(self):
    self.size = 0
    self.owner = None
    self._squares = []
