"""Este módulo fornece uma classe com métodos que manipulam o Banco de Dados do servidor. 
"""

import csv

class ManageDB:
    def __init__(self,path):
        """Inicializa um objeto passando o nome do arquivo .csv na variável 'path'
        """
        self.path = path

    def get_fieldnames(self):
        """Retorna os fieldnames do cabeçalho usados na indexação dos dados nos arquivos.csv
        """
        if self.path == 'voters.csv':
            return ['Nome','CPF']
        elif self.path == 'candidates.csv':
            return ['Nome','Número']
        elif self.path == 'results.csv':
            return ['Nome','Votos']
        elif self.path == 'menu.csv':
            return ['Index','Option']

    def write_headers(self):
        """Escreve o cabeçalho dos arquivos.csv
        """
        with open(self.path, 'w', newline ='') as csvfile:
            fieldnames = self.get_fieldnames()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    def write_file(self,field0, field1):
        """Adiciona uma linha no arquivo.csv passando os valores como parâmetros
        """
        with open(self.path, 'a', newline ='') as csvfile:
            fieldnames = self.get_fieldnames()

            writer = csv.DictWriter(csvfile,fieldnames = fieldnames)
            writer.writerow({fieldnames[0]: field0, fieldnames[1]:field1})

    def read_file(self):
        """Lê um arquivo.csv
        """
        with open(self.path, 'r',newline='')as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = self.get_fieldnames()
            for row in reader:
                print(row[fieldnames[0]],row[fieldnames[1]])
    
    def update_files(self,fieldname,replace):
        with open(self.path, 'r+',newline='')as csvfile:
            reader = csv.DictReader(csvfile)
            reader.readrow()
        
    
m = ManageDB('menu.csv')
m.write_headers()
