"""Este módulo fornece uma classe com métodos que manipulam o Banco de Dados do servidor. 
"""

import csv

class ManageDB:
    def __init__(self,path):
        """Instância um objeto ManageDB passando o path (arquivo.csv) como argumento.
        """
        self.path = path
        self.fieldnames = self.get_fieldnames()
    
    def get_fieldnames(self):
        """Retorna uma lista contendo os fieldnames do arquivo.csv.
        """
        with open(self.path,'r') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                return row

    def read_file(self):
        """Lê um arquivo e o imprime na tela.
        """
        with open(self.path,'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                print (row)

    def write_line(self,dict):
        """Acrescenta uma linha no arquivo, o argumento(linha) deve ser do tipo Dicionário.
        """
        with open(self.path,'a') as csv_file:
            writer = csv.DictWriter(csv_file,fieldnames=self.fieldnames)
            writer.writerow(dict)

    def update_line(self,key,dict):
        """Substitui uma linha do arquivo,os argumentos devem ser um fieldname e um Dicionário respectivamente.
        """
        with open(self.path,'r') as csv_file:
            reader = csv.DictReader(csv_file)

            with open('temp.csv','w') as temp_file:
                writer = csv.DictWriter(temp_file,fieldnames=self.fieldnames)
                writer.writeheader()
                for row in reader:
                    if row[key] == dict[key]:
                        writer.writerow(dict)
                    else:
                        writer.writerow(row)
        with open('temp.csv','r') as temp_file:
            content = temp_file.read()
            
            with open(self.path,'w') as csv_file:
                csv_file.write(content)