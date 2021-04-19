def get_words():
    """Fixes tags that should be camel case, you should create a txt file of them"""
    with open('camel_case.txt','r') as f:
        camel = f.read().split('\n')
    dicio = {}
    for i in camel:
        dicio[i] = i.lower()
    return dicio

get_words()
def clean_words(text):
    """Same as above"""
    camel = get_words()
    for i in camel:
        text = text.replace(
                '<' + camel[i],
                '<' + i)
        text = text.replace(
                '</' + camel[i],
        '</' + i) 
    return text

def load_file(filename):
    with open(filename, 'r') as f:
        text = clean_words(f.read())
    return text

def separate_meta(text):
    text = text.split('\n')
    metadata = []
    data = []
    meta = 0
    for i in text:
        if '<body>' in i:
            meta += 1
        if meta == 0:
            metadata.append(i)
        else:
            data.append(i)
    return ('\n'.join(metadata), '\n'.join(data))

def solve_file(filename, tofile, flag = False):
    """Removes flag errors assigned by work_stanza.py to highlight the presence of 
    enclitics (esp. for Spanish)"""
    text = load_file(filename)
    metadata, data = separate_meta(text)
    text_response = work_around_name(data)
    text_response = remove_un(text_response, flag)
    with open(tofile,'w') as v:
        v.write(metadata)
        v.write('\n')
        v.write(text_response)



def remove_char_name(tos):
    """Converts stanza annotation into TEI format"""
    a, b = tos.split('type="')
    b = b.split('"')
    c = b[0].split("-")
    if len(c) > 1:
        b[0] = c[1]
    b = '"'.join(b)
    tos = a + 'type="' + b
    return tos

def remove_un(text, flag = False):
    """Continuation of the above"""
    text = text.split('\n')
    text_response = []
    close_name = 0
    end = 0
    for index, i in enumerate(text):
        if '<error>' not in i and '<link ana="" target=""/>' not in i:
            if '<name type="' in i:
                text_response.append(remove_char_name(i))
            else:
                text_response.append(i)
        else:
            if flag:
                text_response.append(i)
    return '\n'.join(text_response)


def work_around_name(text):
    """Workaround to deal with name tag"""
    text = text.split('\n')
    text_response = []
    close_name = 0
    end = 0
    for index, i in enumerate(text):
        if end == 1:
            text_response.append(i)
            text_response.append('\t'*2 + '</name>')
            close_name = 0
            end = 0
            continue
        if close_name == 0:
            if '<name type' in i:
                text_response.append(i.replace('</name>', ''))
                close_name = 2
            else:
                text_response.append(i)
            continue
        elif close_name == 1:
            if '<name type' not in i:
                text_response.append('\t'*2 + '</name>')
                text_response.append(i)
                close_name -= 1
            else:
                close_name = 2
                if '<name type="E-' in i:
                    end = 1
            continue
        elif close_name == 2:
            if '<name type' not in i:
                text_response.append(i)
                close_name -= 1
            continue
        else:
            text_response.append('error_here')
            continue
    return '\n'.join(text_response)

import os
files = os.listdir('result/')
# Renames files to ana.xml. Creates two sets with error flags and no flags 
# (error flags could be used for a manual fix).
for index, file in enumerate(files):
    print(index)
    solve_file('result/' + file,
            'noflag/' + file.replace('.xml','') + '.ana.xml',
            flag = False)

for index, file in enumerate(files):
    print(index)
    solve_file('result/' + file,
            'flag/' + file.replace('.xml','') + '.ana.xml',
            flag = True)
