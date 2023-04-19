import ifcopenshell

#---importar ifc y parsarlo a una variable
ifc = ifcopenshell.open(r"C:\Users\Acer\OneDrive - Syncroniza Spa\Desktop\Syncroniza\python\IFC-Python\OpenShell-IFC\mad_scientist_212.ifc")

#---IfcSpace (esternal ID: #194)
#icfSpace = ifc.by_type("IfcSpace")
#print(icfSpace)

#---Pedir todas las murallas
wall = ifc.by_type("IfcWall")
#print(wall)

#---pedir una muralla or su id
wall = ifc.by_guid("2sEeFec9X798gqrB4DTSWW")
print(wall)
#---preguntar el tipo de entidad
#print(wall.is_a())
#---preguntar si es un tipo de entidad x .Devuelve un boleano
#print(wall.is_a("IfcWall"))
#---PredefinedType. es el atributo que puede tener una entidad, por ejemplo un muro

#print(wall.PredefinedType) ############___REVISAR___#########

#---preguntar el ID de un objeto
#print(wall.GlobalId)
#---preguntar el nombre de un objeto
#print(wall.Name)
#---propertySet: son lo más importante.
#---preguntar las propiedades de un objeto
#print(wall.IsDefinedBy)
#---preguntar la RelatingPropertyDefinition
#rel = wall.IsDefinedBy[0]
#pset = rel.RelatingPropertyDefinition
#print(pset)
#---preguntar las propiedades del objeto
#print(pset.HasProperties)