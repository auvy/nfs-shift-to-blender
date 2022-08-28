
class theme():
    def __init__(self, name, size, offset):
        self.name 	= name
        self.size 	= size
        self.offset = offset

class elmts():
    def __init__(self, firstAttr,numAttrs,numChildren,firstChild,nextSibling):
        self.firstAttr 		= firstAttr
        self.numAttrs 		= numAttrs
        self.numChildren 	= numChildren
        self.firstChild 	= firstChild
        self.nextSibling 	= nextSibling

class attrs():
    def __init__(self, ID,type,val,num_values,nextAttr):
        self.ID 				= ID
        self.type 			= type
        self.val 				= val
        self.num_values = num_values
        self.nextAttr 	= nextAttr

class colls():
    def __init__(self, ID,unknown1,unknown2,unknown3):
        self.ID 			= ID
        self.unknown1 = unknown1
        self.unknown2 = unknown2
        self.unknown3 = unknown3

class amatrix():
    def __init__(self, position,orientation):
        self.position 			= position
        self.orientation = orientation
