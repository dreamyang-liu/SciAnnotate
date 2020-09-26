import re
from document import real_directory
from os.path import join as path_join
from os.path import join as path_join
from os.path import split as path_split
from jsonwrap import dumps as json_dumps
from jsonwrap import loads as json_loads
from utils import get_entity_index_exist, get_entity_index, add_common_info, annotation_file_generate,parse_annotation_file

def create_span_all_text(**kwargs):
    label = kwargs['label']
    collection = kwargs['collection']
    document = kwargs['document']
    keyword = kwargs['keyword']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.txt'
    ann_file_path = txt_file_path[:-3] + 'ann'
    return _create_span_all_text(txt_file_path, ann_file_path, keyword, label)

def _create_span_all_text(txt_file_path, ann_file_path, keyword, label, entity_index = get_entity_index_exist):
    res = dict()
    with open(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open(ann_file_path, 'r') as ann_file:
        ann = ann_file.read()

    exist_index = ann.split('\n').__len__()
    
    entity_index = get_entity_index_exist(exist_index)

    entities = [
        ["T" + str(next(entity_index)), label, [(pos.start(), pos.end())]]
        for pos in re.finditer(keyword, text)
    ]
    res["entities"] = entities
    annotation_file_generate(res, ann_file_path, text, 'a')
    cur_anns = parse_annotation_file(ann_file_path)
    cur_entities = []
    for cur_ann in cur_anns:
        try:
            if cur_ann:
                cur_entities.append([cur_ann.id, cur_ann.type, cur_ann.spans])
        except AttributeError:
            pass
    res['entities'] = cur_entities
    res = add_common_info(text, res)
    
    return res

def create_span_all_re(**kwargs):
    directory = kwargs["collection"]
    document = kwargs["document"]
    keyword = kwargs["keyword"]
    label = kwargs["label"]
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.txt'
    ann_file_path = txt_file_path[:-3] + '.ann'
    return _create_span_all_re(txt_file_path, ann_file_path, keyword, label)

def _create_span_all_re(txt_file_path, ann_file_path, keyword, label):
    res = dict()
    with open_textfile(txt_file_path, 'r') as txt_file:
        text = txt_file.read()
    with open_textfile(ann_file_path, 'r') as ana_file:
        ann = ann_file.readlines()
    for line in ann:
        entity_index = line.split(" ")
        entity_index = entity_index[0][1:]
    
    entity_index = get_entity_index()

    regx = re.compile(keyword)
    entities = [
        ["T" + str(next(entity_index)), label, [(pos.start(), pos.end())]]
        for pos in regx.finditer(text)
    ]
    res["entities"] = entities
    
    return entities