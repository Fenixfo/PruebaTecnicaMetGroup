class MyMatrix:
  def __init__(self,matrix,value=1,longi=0,machine=-1):
    self.matrix = matrix
    self.value = value
    self.longi=longi
    self.compute=0
    self.dimension=0
    self.straight=0
    if machine==-1:
      self.compute=MyMatrix(self.matrix,machine=1).computeMethod()
      self.dimension=MyMatrix(self.matrix,machine=1).dimensionMethod()
      self.straight=MyMatrix(self.matrix,machine=1).straightMethod()

  def computeMethod(self):
    value=0
    for i in self.matrix:
      #verificar si el valor a revisar es un número
      if type(i)!=list:
        value+=i
      else:
        # suma recursiva
        value+=MyMatrix(i,machine=1).computeMethod()
    return value

  def dimensionMethod(self):
    sum=0
    data=0
    #verificar si el valor a revisar es un número
    if type(self.matrix)!=list:
      return(self.value)
    #recorrer el arreglo
    for i in self.matrix:
      #verificar si el valor a revisar es un número
      if type(i)!=list:
        data+=1
    #verificar si todos los datos en el arreglo son números
    if len(self.matrix)==data:
      return(self.value)
    else:
      for i in self.matrix:
        #recursión para las listas restantes
        returnValue=MyMatrix(i,self.value+1,machine=1).dimensionMethod()
        #verificación de nivel máximo
        if returnValue>sum:
          sum=returnValue
    return(sum)
  #este es el método para sacar el número de elementos en las listas
  def cuadro(self):
    tam = len(self.matrix)
    data=0
    for i in self.matrix:
      #verificar si el valor a revisar es un número
      if type(i)!=list:
        data+=1
    #verificar si hay números y listas en el mismo nivel de lista
    if tam!=data and data!=0:
      return -1
    #verificar si solo son números en el nivel actual
    if data==tam:
      #mediante recursión se verifica que los demás niveles tengan el mismo peso
      if self.longi!=0 and data!=self.longi:
        return -1
      return data
    #verificar que no hay números en el nivel actual
    if data==0:
      returnValue=0
      for i in self.matrix:
        #recursión para visitar los demás niveles
        returnValue=MyMatrix(i,longi=returnValue,machine=1).cuadro()
        if returnValue==-1:
          return -1
      return returnValue
  #método que verifica si en verdad es un "cuadro"(matriz uniforme) el valor -1 significa que no es uniforme, cualquier otro valor representa uniformidad
  def straightMethod(self):
    if MyMatrix(self.matrix,machine=1).cuadro()==-1:
      return False
    else:
      return True

#definir las listas
a = [1,2]
b = [[1,2],[2,4]]
c = [[1,2],[2,4],[2,4]]
d = [[[3,4],[6,5]]]
e = [[[1, 2,3]], [[5, 6, 7],[5, 4, 3]], [[3, 5, 6], [4, 8, 3], [2, 3]]]
f = [[[1, 2, 3], [2, 3, 4]], [[5, 6, 7], [5, 4, 3]], [[3,5, 6], [4, 8, 3]]]
#ejercicio A
print('ejercicio A')
print(MyMatrix(a).compute)
print(MyMatrix(b).compute)
print(MyMatrix(c).compute)
print(MyMatrix(d).compute)
print(MyMatrix(e).compute)
print(MyMatrix(f).compute)
#ejercicio B
print('ejercicio B')
print(MyMatrix(a).dimension)
print(MyMatrix(b).dimension)
print(MyMatrix(c).dimension)
print(MyMatrix(d).dimension)
print(MyMatrix(e).dimension)
print(MyMatrix(f).dimension)
#ejercicio C
print('ejercicio C')
print(MyMatrix(a).straight)
print(MyMatrix(b).straight)
print(MyMatrix(c).straight)
print(MyMatrix(d).straight)
print(MyMatrix(e).straight)
print(MyMatrix(f).straight)
