# coding: utf-8


import codecs
import requests
import lxml.objectify as obj

record_base = 'https://www.re3data.org/api/v1/repository/'          # url do site fixada
repository_list = 'https://www.re3data.org/api/v1/repositories'     # lista de repositorios a serem extraídos

html = requests.get(repository_list, timeout=10).content            # html <- codigo da pagina
print(html)
tree = obj.fromstring(html)    # inicializa arvore de dados para parsing
with codecs.open('../dados/RepoListAPI.tsv', 'w', 'utf-8-sig') as records:   # abre arquivo para escrito
    records.write('Link\tName\n')                                   # headers do arquivo
    for item in tree.getchildren():                                 # percorre arvore de dados
        if '\n' not in '%s' % item.name:                            # testa se há caracter '\n' na linha atual
            records.write('%s\t%s\n' % (record_base + item.id, item.name))      # escreve linha no arquivo
        else:
            records.write('%s\t%s' % (record_base + item.id, item.name))
records.close()     # fecha arquivo de output
print(repository_list)
