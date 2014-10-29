import os
import datetime
from types import *
class config:

   def __init__(self,phFilePlugin):
      self.matriceOpzioni = []
      self.pathFilePlugin = phFilePlugin
      self.nomeFile = ""
      self.leggiFileOpzioni()

   def leggiFileOpzioni(self):

      self.nomeFile = os.path.join(self.pathFilePlugin,"configurazione/configurazione.txt")
      if os.path.isfile(self.nomeFile):
         inFile = open(self.nomeFile)
         while True:
            riga = inFile.readline()
            if riga == "":
               break
            lista_campi = riga.split('\t')
            ucampo = lista_campi[-1]
            uc = ucampo[-1]
            while uc == "\t" or uc == "\n" or uc == "\r" :
               ucampo = ucampo.rstrip(uc)
               uc = ucampo[-1]
            lista_campi[-1] = ucampo
            self.matriceOpzioni.append(lista_campi)
         inFile.close()

   def cercaOpzione(self,nomeOpzione):
      for j in self.matriceOpzioni:
         if nomeOpzione == j[0]:
            if j[1] == 'True':
               return True
            if j[1] == 'False':
               return False
            return j[1]
      if nomeOpzione == "SAVE_PRG_BEFORE_DB_CONN":
         return True
      return ""
   def impostaOpzione(self,nomeOpzione,valore):
      if type(valore) == BooleanType:
         if valore :
            valore ='True'
         else:
            valore ='False'
      for j in self.matriceOpzioni:
         if nomeOpzione == j[0]:
            j[1] = valore
            return True
      self.matriceOpzioni.append([nomeOpzione,valore])
      return False
   def salvaFileOpzioni(self):
      os.rename(self.nomeFile,self.nomeFile+"_old_"+datetime.datetime.now().strftime("%d%m%Y_%H%M%S")+".txt")
      outFile = open(self.nomeFile,"w")
      for j in self.matriceOpzioni:
         riga = ""
         for k in j:
            riga += k +"\t"
         rigaout = riga.rstrip('\t')
         rigaout = rigaout + "\n"
         outFile.write(rigaout)
      outFile.close()
