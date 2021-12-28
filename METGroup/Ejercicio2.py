class MyArray:
  def __init__(self,cadena):
    self.cadena = cadena
    #Se definen como falso por defecto
    self.operation = False
    self.compute = False
    try:
      # Si no ocurre un error significa que es correcta la operación y se asignan nuevos valores
      self.compute=eval(self.cadena)
      self.operation=True
    except:
      pass

a = "Hello world" 
b = "2 + 10 / 2 - 20" 
c = "(2 + 10) / 2 - 20" 
d = "(2 + 10 / 2 - 20"
#ejercicio A
print('ejercicio A')
print(MyArray(a).operation)
print(MyArray(b).operation)
print(MyArray(c).operation)
print(MyArray(d).operation)
#ejercicio B
print('ejercicio B')
print(MyArray(a).compute)
print(MyArray(b).compute)
print(MyArray(c).compute)
print(MyArray(d).compute)
