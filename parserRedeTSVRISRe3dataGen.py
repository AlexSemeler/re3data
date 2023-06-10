# coding: utf-8

from codecs import open

output_file = open('../dados/Rede.ris', 'w', 'utf-8-sig')
table = open('../dados/Re3Data_repositories.tsv', 'r', 'utf-8-sig')
data_list = table.readlines()
table.close()
for i in data_list:
    try:
        output_file.write('TY  - REPO\n')
        i = i.split('\t')
        output_file.write('AU  - %s\n' % i[0])
        output_file.write('DP  - %s\n' % i[3])
        for j in i[-4].split(','):
            output_file.write('PP  - %s\n' % j)
        for k in i[-2].split(','):
            output_file.write('KW  - %s\n' % k)
        for l in i[7].split(','):
            output_file.write('L4  - %s\n' % l)
        output_file.write('ER  - \n')
    except IndexError:
        continue
output_file.close()
