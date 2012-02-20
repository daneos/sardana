##############################################################################
##
## This file is part of Sardana
##
## http://www.tango-controls.org/static/sardana/latest/doc/html/index.html
##
## Copyright 2011 CELLS / ALBA Synchrotron, Bellaterra, Spain
## 
## Sardana is free software: you can redistribute it and/or modify
## it under the terms of the GNU Lesser General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
## 
## Sardana is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Lesser General Public License for more details.
## 
## You should have received a copy of the GNU Lesser General Public License
## along with Sardana.  If not, see <http://www.gnu.org/licenses/>.
##
##############################################################################

"""Examples of macro functions"""

__docformat__ = 'restructuredtext'

__all__ = ["mfunc1", "mfunc2", "mfunc3", "mfunc4"]

from sardana.macroserver.macro import Type, macro

@macro()
def mfunc1():
    """First macro function. No parameters whatsoever"""
    self.output("Executing %s", self.getName())

@macro()
def mfunc2(p1):
    """Second macro function. One parameter of unknown type"""
    self.output("parameter: %s", p1)

@macro([ ["moveable", Type.Moveable, None, "motor to watch"] ])
def mfunc3(moveable):
    """Third macro function. A proper moveable parameter"""
    self.output("Moveable %s is at %s", moveable.getName(), moveable.getPosition())

@macro()
def mfunc4(*args):
    """Fourth macro function. A list of parameters of unknown type"""
    self.output("parameters %s", args)
    
@macro()
def mfunc5(*args):
    """Fifth macro function. A list of parameters of unknown type"""
    self.output("parameters %s", args)
