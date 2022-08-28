import os

from functools import partial
from genericpath import exists


from .binary_stream import BinaryStream
from mathutils import Euler
from math import radians


import bpy

def get_object_by_name(collection, name):
   return bpy.data.collections[collection].all_objects.get(name)


def name_filter(filter, partname, check):
    if check:
        if filter in partname:
            return True
    return False


class attr:
    def __init__(self, ID, type, val, num_values, nextArr):
        self.ID = ID
        self.type = type
        self.val = val
        self.num_values = num_values
        self.nextArr = nextArr

def readBLMY (filename):
    ATTRarr = []
    NUMBarr = []
    
    num_attr = 0
    num_numb = 0
    
    f = open(filename, "rb")
    print(f.tell())
    stream = BinaryStream(f)
    
    f.seek(4, 1)
    numChunks = stream.readULong()
    filesize =  stream.readULong()
    f.seek(4, 1)
    
    for i in range(0, numChunks):
        CHname = ""
        for w in range(0, 4):
            CHname += chr(int.from_bytes(stream.readByte(), 'big'))
        CHsize = stream.readULong()
        CHoffset = stream.readULong()
        f.seek(4, 1)
        
        currentOffset = f.tell()
        f.seek(CHoffset, 1)
        
        if  CHname == 'HEAD':
            num_elmt = stream.readULong()
            num_attr = stream.readULong()
            num_coll = stream.readULong()
            num_numb = stream.readULong()
            num_strs = stream.readULong()
            unknown1 = stream.readULong()
            unknown2 = stream.readULong()
        elif CHname == 'ATTR':
            for i in range(0, num_attr):
                ID          = stream.readULong()
                type        = stream.readULong()
                val         = stream.readULong()
                num_values  = stream.readULong()
                nextAttr    = stream.readULong()
                ATTRarr.append(attr(ID, type, val, num_values, nextAttr))
        elif CHname == 'NUMB':
            for i in range(0, num_numb):
                NUMBarr.append(stream.readFloat())
        elif CHname == 'STRS':
            STRSoffset = CHoffset
        f.seek(currentOffset, 1)


def import_part(filename, rotate, ignore_damage, lodb, lodc):
    farr = []
    vertarr = []
    UVarr = []
    faceMatID = []
    normarr = []
    hasnormals = False
    OBJstring = ''
    colorArr = []

    f = open(filename, "rb")
    print(f.tell())
    stream = BinaryStream(f)

    b1 = f.read(1)
    b2 = f.read(1)
    b3 = f.read(1)
    b4 = f.read(1)
    b5 = f.read(1)
    b6 = f.read(1)
    b7 = f.read(1)
    b8 = f.read(1)

    partName = stream.readStr()



    if 'dmg' in filename:
        if ignore_damage:
            return
        partName += '_DMG'
    print("Loading part: " + partName)

    pos = f.tell()
    print(pos)
    modulo = pos % 4
    # if modulo != 0:
    move = 4 - modulo
    f.seek(move, 1)

    numVerts      = stream.readULong()
    numVertProps  = stream.readULong()
    numPrims      = stream.readULong()

    #skip 40
    f.seek(40, 1)

    if int.from_bytes(b5, "big") == 1:
        numbones = stream.readULong()
        numchars = stream.readULong()
        f.seek(numchars, 1)
        f.seek(numbones * 48, 1)
        
    #vertex props
    print(f"vertprops {numVertProps}")
    for prop in range (0, numVertProps):
        rec1 = stream.readULong()
        rec2 = stream.readULong()
        rec3 = stream.readULong()
        vProp = str(rec1) + str(rec2) + str(rec3)
           
        #positions     
        if vProp == '200':
            for v in range(0, numVerts):
                vx = stream.readFloat()
                vy = stream.readFloat()
                vz = stream.readFloat()
                
                OBJstring += f"v {str(round(vx, 8))} {str(round(vz, 8))} {str(round(vy, 8))}\n"
                vertarr.append((vx, vy, vz))
                
            OBJstring += f"# {numVerts} vertices\n\n"
        
        #colors
        elif vProp == '460':
            for c in range (0, numVerts):
                colorArr.append([stream.readByte(), stream.readByte(), stream.readByte(), stream.readByte()])
        
        #skip colors2
        elif vProp == '461':
            f.seek(numVerts * 4, 1)
        
        #normals
        elif vProp == '220':
            for n in range (0, numVerts):
                nx = stream.readFloat()
                ny = stream.readFloat()
                nz = stream.readFloat()
                OBJstring += f"vn {str(round(nx, 8))} {str(round(nz, 8))} {str(round(ny, 8))}\n"
            OBJstring += f"# {numVerts} vertex normals\n\n"
        
        #skip tangents
        elif vProp == '240' or vProp == '250':
            f.seek(numVerts * 12, 1)
        
        #UV 
        elif vProp == '130' or vProp == '131' or vProp == '132' or vProp == '133' or vProp == '134':
            print(f"called UV for some reason {vProp}")
            for v in range(0, numVerts):
                UVu = stream.readFloat()
                UVv = (1 - stream.readFloat())
                # OBJstring += f"vt {str(round(UVu, 8))} {str(round(UVv, 8))}\n"
                
                UVarr.append([[UVu, UVv, 0.0], vProp])
            OBJstring += f"# {numVerts} vertex textures idk\n\n"
        
        #UVW   
        elif vProp == '230' or vProp == '231' or vProp == '232' or vProp == '233' or vProp == '234':
            print(f"aclled {vProp}")
            for v in range(0, numVerts):
                UVu = stream.readFloat()
                UVv = 1 - stream.readFloat()
                UVw = stream.readFloat()
                #OBJstring += f"vt {str(round(UVu, 8))} {str(round(UVv, 8))}\n"
                UVarr.append([[UVu, UVv, UVw], vProp])
        
        #skip zeroes
        elif vProp == '033':
            f.seek(numVerts * 4, 1)
            
        #skip indices? idk
        elif vProp == '580':
            f.seek(numVerts * 4, 1)
            
        #skip bone weights idk
        elif vProp == '310':
            f.seek(numVerts * 16, 1)
    
    #end reading vertices
    OBJstring += f"g {partName}\n"

    print(f'uvarr len {len(UVarr)}')
    print(f'vert len {numVerts}')

    print(f"numprims {numPrims}")
    
    #start reading faces
    for p in range(0, numPrims):
        mexfile = stream.readStr()
        matname = os.path.basename(mexfile)[:-4]
        print(f"mat {matname}")
        
        #jump alignment zero bytes??
        pos = f.tell()
        modulo = pos % 4
        # if modulo != 0:
        move = 4 - modulo
        f.seek(move, 1)
        
        
        #jump one long of zeroes
        f.seek(4, 1)
        
        print(f.tell())
        numFaces = stream.readLong()
        print(f"numfaces {numFaces}")
        print(f.tell())
        OBJstring += f"usemtl {matname}\n"
                
        #jump skeleton shorts
        if int.from_bytes(b5, "big") == 1:
            numshorts = stream.readLong()
            f.seek(numshorts * 2, 1)
        
        #jump alignment zero bytes
        pos = f.tell()
        modulo = pos % 4
        if modulo != 0:
            move = 4 - modulo
            f.seek(move, 1)
        
        print(f.tell())
        
        #read faces
        for face in range(0, numFaces):
            ind1 = (stream.readUInt16()) + 1
            ind2 = (stream.readUInt16()) + 1
            ind3 = (stream.readUInt16()) + 1
            OBJstring += f"f {ind3}//{ind3} {ind2}//{ind2} {ind1}//{ind1}\n"
        
        #jump alignment zero bytes
        pos = f.tell()
        modulo = pos % 4
        if modulo != 0:
            move = 4 - modulo
            f.seek(move, 1)
            
        #read 2 shorts of some face index idk
        short1 = stream.readUInt16()
        short2 = stream.readUInt16()
        
        #jump 10 float
        f.seek(40, 1)
    
    f.close()
    
    # amesh
    ok = int(len(UVarr)/numVerts)
    print(f"ok {len(UVarr)}")
    
    objname = partName
    
    objloc = f"{bpy.app.tempdir}\\{objname}.obj"   
    
    text_file = open(objloc, "w")
    text_file.write(OBJstring)
    text_file.close()
    
    bpy.ops.import_scene.obj(filepath=objloc, split_mode='OFF')
    os.remove(objloc)

    objs = bpy.context.selected_objects
    body = ''
    for obj in objs:
        print(f"objname {obj.name}")
        if objname in obj.name:
            body = obj
            print(f"selected {obj.name}")
            break

    me = body.data

    for uv in range(0, ok):
        #create new map for object and select it
        me.uv_layers.new(name=f'MEBUVLayer{uv}')
        selectedUV = me.uv_layers[f'MEBUVLayer{uv}']
        
        for loop in me.loops:
            UVu = UVarr[loop.vertex_index + numVerts * uv][0][0]
            UVv = UVarr[loop.vertex_index + numVerts * uv][0][1]
            selectedUV.data[loop.index].uv = (UVu, UVv)     
            
    if rotate:
        body.rotation_euler = Euler((radians(180), radians(180), radians(180)), 'XYZ')
        
    if lodb:
        if 'LODB' in partName:
            body.hide_set(True)
    
    if lodc:
        if 'LODC' in partName:
            body.hide_set(True)

            
        
    
def load(filepath, importall, rotate, damage, lodb, lodc):
        if importall:
            mebdir = os.path.dirname(filepath)
            for file in os.listdir(mebdir):
                if file.lower().endswith(".meb"):
                    import_part(os.path.join(mebdir, file), rotate, damage, lodb, lodc)
        else:
            import_part(filepath, rotate, damage, lodb, lodc)