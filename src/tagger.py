import json


def tagRegrex(position):
    '''
    You can add your custom regex for a job description and
    maintain it next to the position key in the regex.json file
    '''
    with open('./src/.res/regex.json') as file:
        tag_regrex = json.load(file)
        if position in tag_regrex.keys():
            tag_regrex = tag_regrex[position]
        else:
            tag_regrex = tag_regrex['Default']
        return tag_regrex
