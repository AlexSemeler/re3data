# -*- coding: utf-8 -*-

import codecs
import requests
import lxml.objectify as obj
import lxml.etree


def extract_item(field, item, a_tuple, index, namespace):
    if namespace + field == item.tag:
        a_tuple[index] = item
        return True
    return False


def extract_list_item(field, item, a_tuple, index, namespace):
    if namespace + field == item.tag:
        a_tuple[index].append(item)
        return True
    return False


with codecs.open('../dados/RepoListAPI.tsv', 'r', 'utf-8-sig') as api_file:     # necessario comentar o codigo
    link_list = api_file.readlines()[1:]
    api_file.close()

errors = 0

reps = codecs.open('../dados/Re3Data_repositories.tsv', 'w', 'utf-8-sig')
reps.write('Name\tDescription\tURL\tSoftware Name\tLicense\tData Acess Type\tRep. Type\tContent Type\tRep. Language\t'
           'Institution\tCountry\tInst. Type\tKeyword\tSubject\n')
reps.close()

namespaces = {'r3d': ''}
list_size = len(link_list) - 1
print('PARSING START,', list_size, 'repositories listed')
for i in range(len(link_list)):
    log = open('../dados/error_logs/re3dataCSVgenErrorLog.txt', 'a')
    try:
        html = requests.get(link_list[i].split('\t')[0], timeout=10).content
        tree = obj.fromstring(html)
    except requests.exceptions.SSLError:
        print('SSL error with %s Parsing aborted.' % link_list[i])
        log.write('SSL error with: %s\n' % link_list[i])
        errors += 1
        continue
    except requests.exceptions.ReadTimeout:
        print('Read timed out with %s.' % link_list[i])
        log.write('Read timed out with: %s\n' % link_list[i])
        errors += 1
        continue
    except requests.exceptions.Timeout:
        print('Connection timeout with %s Parsing aborted.' % link_list[i])
        log.write('timeout with: %s\n' % link_list[i])
        errors += 1
        continue
    except lxml.etree.XMLSyntaxError:
        print('XML syntax error with %s.' % link_list[i])
        log.write('XML syntax error with: %s\n' % link_list[i])
        errors += 1
        continue
    with codecs.open('../dados/Re3Data_repositories.tsv', 'a', 'utf-8-sig') as reps:
        namespaces['r3d'] = tree.tag.split('}')[0] + '}'
        tree = tree.repository
        writing_tuple = [0, 0, 0, 0, 0, 0, [], [], [], [], [], [], [], []]
        print('PARSING:', i, 'from', list_size)
        for child in tree.getchildren():
            if extract_item('repositoryName', child     , writing_tuple, 0, namespaces['r3d']):
                continue
            #if extract_item('description', child, writing_tuple, 1, namespaces['r3d']):
                #continue
            if extract_item('repositoryURL', child, writing_tuple, 2, namespaces['r3d']):
                continue
            if namespaces['r3d'] + 'software' == child.tag:
                writing_tuple[3] = child.softwareName
                continue
            if namespaces['r3d'] + 'dataLicense' == child.tag:
                writing_tuple[4] = child.dataLicenseName
                continue
            if namespaces['r3d'] + 'dataAccess' == child.tag:
                writing_tuple[5] = child.dataAccessType
                continue
            if extract_list_item('type', child, writing_tuple, 6, namespaces['r3d']):
                continue
            if extract_list_item('contentType', child, writing_tuple, 7, namespaces['r3d']):
                continue
            if extract_list_item('repositoryLanguage', child, writing_tuple, 8, namespaces['r3d']):
                continue
            if namespaces['r3d'] + 'institution' == child.tag:
                writing_tuple[9].append(child.institutionName)
                writing_tuple[10].append(child.institutionCountry)
                writing_tuple[11].append(child.institutionType)
                continue
            if extract_list_item('keyword', child, writing_tuple, 12, namespaces['r3d']):
                continue
            if extract_list_item('subject', child, writing_tuple, 13, namespaces['r3d']):
                continue
        for j in range(0, 6):
            reps.write('%s'.replace('\t', '').replace('\n', '') % writing_tuple[j] + '\t')
        for j in range(6, len(writing_tuple)):
            limit = len(writing_tuple[j])
            for k in range(0, limit):
                if k < limit - 1:
                    reps.write('%s, '.replace('\t', '').replace('\n', '') % writing_tuple[j][k])
                else:
                    if j < len(writing_tuple) - 1:
                        reps.write('%s'.replace('\t', '').replace('\n', '') % writing_tuple[j][k] + '\t')
                    else:
                        reps.write('%s'.replace('\t', '').replace('\n', '') % writing_tuple[j][k] + '\n')
    reps.close()
    log.close()
print('WRITING ENDED, output file shall have', list_size, 'lines.\n', errors, 'had errors.')
