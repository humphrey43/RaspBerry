'''
Created on 07.02.2016

@author: hardy
'''
import json

'''class ClassFactory:
    def __init__(self):
        self.classes = {}

    def register(self, name, clazz):
        self.classes[name] = clazz
    
    def createInstance(self, objdef):
        erg = None
        name = ""
        objdict = None
        
        if objdef[0] == '{':
            objdict = json.loads(objdef)
            name = objdict["__class_name__"]
        else:
            name = objdef
            
        clazz = self.classes[name]
        if not clazz is None:
            erg = clazz()
            if not objdict is None:
                for k, v in objdict.iteritems():
                    setattr(erg, k, v)
        return erg
'''

registeredClasses = {}

def registerClass(name, clazz): 
    registeredClasses[name] = clazz
       
def toJSON(obj):
    return json.dumps(obj.__dict__)

def createInstance(objdef):
    erg = None
    name = ""
    objdict = None
    
    if objdef[0] == '{':
        objdict = json.loads(objdef)
        name = objdict["__class_name__"]
    else:
        name = objdef
        
    clazz = registeredClasses[name]
    if not clazz is None:
        erg = clazz()
        if not objdict is None:
            for k, v in objdict.iteritems():
                setattr(erg, k, v)
    return erg

class CallbackInfo:
    
#    callback_object = None
#    callback_method = None
    
    def __init__(self, method):
#        self.callback_object = obj
        self.callback_method = method

    def call(self, *parm):
#        if self.callback_object is not None:
#            o = self.callback_object
        m = self.callback_method
        m(parm)

def get_instance_of_class( kls ):
    c = get_class(kls)
    return c()

def get_class( kls ):
    parts = kls.split('.')
    module = ".".join(parts[:-1])
    m = __import__( module )
    for comp in parts[1:]:
        m = getattr(m, comp)            
    return m