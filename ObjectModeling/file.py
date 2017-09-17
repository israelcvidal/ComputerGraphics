from object import Obj

def import_obj(name):
    obj = Obj()
    with open(name) as file:
        for line in file:
            array = line.split()
            if (array[0] == 'v'):
                obj.add_vertex(array[1], array[2], array[3])
            if (array[0] == 'f'):
                obj.add_face(array[1], array[2], array[3])
        return obj