
import win32print
import win32api
import os

# Lista impressoras disponíveis
lista_impressoras = win32print.EnumPrinters(2)
print("Lista de impressoras:", lista_impressoras)