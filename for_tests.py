import re

text = "https://spb.hh.ru/vacancy/84018264?from=vacancy_search_list&query=python"

t = re.search('\d+', text).group()

print(t)
