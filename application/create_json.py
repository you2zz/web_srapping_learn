import json


def create_json(data_in ):
    with open('data/vacancy_parsed.json', 'w', encoding='utf-8') as file:
        json.dump(data_in, file, indent=4, ensure_ascii=False)