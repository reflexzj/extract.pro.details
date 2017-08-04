# coding=utf-8


def get_entitys(row):
    '''
    统计中文字符串中，对应实体的种类和个数
    :param ch: 通过斯坦福coreNLP中文模型工具，将每行句子中的中文实体提取，逐行存入ch.txt文件中去
    :return: 返回对应行，实体种类以及数目
    '''
    entitys = []
    count = {}
    ch_alls = row.strip().split(' ')

    for entity in ch_alls:
        if entity not in entitys:
            entitys.append(entity)
            count[entity] = 1
        else:
            count[entity] += 1

    return entitys, count


def match_rule(rules, entitys, count):
    '''
    判断当前的句子符不符合规则，返回boolean值
    :param rules: 规则：实体种类、每类个数范围，career = {'ORGANIZATION': [1,10], 'DATE': [0,5], 'TITLE':[1,5], 'PERSON': [0,1]}
    :param entitys:
    :param count:
    :return:
    '''

    for rule in rules.keys():
        # 包含规则内的实体，是否满足范围
        if rule in entitys:
            if count[rule] < rules[rule][0] or count[rule] > rules[rule][1]:
                return False
        # 规则内要求的实体不存在时，看看该实体能否为0
        else:
            if rules[rule][0] > 0:
                return False

    return True


def give_sentences(ch, rule, fp):
    """
    返回满足规则的句子，写到fp文件中去
    :param ch: 对应实体表（每行句子的实体都被提取出来）
    :param rule: 给定的规则
    :param fp:
    :return:
    """
    lines = []
    ch_lines = ch.readlines()
    rows = len(ch_lines)

    # 逐行读取，将满足规则句子所在行号记录下来（entitys[0]记录的就是行号，从1开始）
    for i in range(rows):
        entitys, count = get_entitys(ch_lines[i])
        if match_rule(rule, entitys, count):
            lines.append(int(entitys[0]))

    result = open('../data/selected_mess/sentences/sentences.txt', 'r')
    result_lines = result.readlines()

    tags = open('../data/selected_mess/sentences/tags.txt', 'r')
    tags_lines = tags.readlines()

    flag = ''
    for line in lines:
        data = result_lines[line - 1]
        print data.strip('\n')
        tag = tags_lines[line - 1].split(' ')
        name = tag[0]
        college = tag[1]
        company = tag[2].strip('\n')

        if flag == name:
            fp.write( data.strip('\n') + '。')
        else:
            flag = name
            fp.write('\n'+ flag+ ','+ college+','+ company+ ',')




if __name__ == "__main__":
    ch = open('../data/extract_info/ch.txt', 'r')

    career_csv = open('../data/extract_info/final_result/career.csv', 'w')
    contribute_csv = open('../data/extract_info/final_result/contribute.csv', 'w')
    area_csv = open('../data/extract_info/final_result/area.csv', 'w')

    career = {'ORGANIZATION': [1,5], 'DATE': [0,5], 'TITLE':[1,5], 'PERSON': [0,0], 'ORDINAL':[0,0] }
    contribute = {'ORGANIZATION': [1,10], 'ORDINAL':[0,2], 'DATE':[0,2], 'PERSON': [0,0]}
    article = {}
    area = {'O':[2,20]}

    # 是否要注意次序，成果，生涯，领域要一次提取？
    give_sentences(ch, contribute, contribute_csv)
    # give_sentences(ch, career, career_csv)
    # give_sentences(ch, area, area_csv)









