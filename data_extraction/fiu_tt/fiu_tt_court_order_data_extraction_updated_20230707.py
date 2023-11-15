import re
import pandas as pd

with open('fiu_tt_court_order_raw_data_20230707.txt', 'r') as file:
    document_text = file.read()

# remove all instances of Claimant and Defendant
document_text = document_text.replace("Claimant", "").replace("Defendant", "")


# Define the pattern to find occurrences of "BETWEEN THE ATTORNEY GENERAL OF TRINIDAD AND TOBAGO AND"
pattern = re.compile(r'BETWEEN\s+THE\s+ATTORNEY\s+GENERAL\s+OF\s+TRINIDAD\s+AND\s+TOBAGO\s+AND', re.IGNORECASE)
pattern2 = re.compile(r'BETWEEN\s*THE\s*ATTORNEY\s*GENERAL')
matches = pattern.finditer(document_text)

result = []

for match in matches:
    start_index = match.end()

    # get all the text after 'BETWEEN THE ATTORNEY GENERAL OF TRINIDAD AND TOBAGO AND'
    next_text = document_text[start_index:]
    next_text = next_text.strip()

    # get the text before the next instance of 'BETWEEN THE ATTORNEY GENERAL'
    match2 = pattern.search(next_text)
    if match2:
        before_between_text = next_text[:match2.start()].strip()
        before_between_text = before_between_text.strip()  # remove leading and trailing whitespaces
        # split by 'details of order'
        before_details_of_order = re.split(r'details of order', before_between_text, flags=re.IGNORECASE)
        before_details_of_order = before_details_of_order[0].strip()
        before_details_of_the_order = re.split(r'details of the order', before_details_of_order, flags=re.IGNORECASE)
        before_details_of_the_order = before_details_of_the_order[0].strip()
        # split by 'it is hereby declared'
        before_it_is_hereby = re.split(r'it is hereby declared', before_details_of_the_order, flags=re.IGNORECASE)
        before_it_is_hereby = before_it_is_hereby[0].strip()
        before_it_is_declared = re.split(r'it is declared', before_it_is_hereby, flags=re.IGNORECASE)
        before_it_is_declared = before_it_is_declared[0].strip().replace("and also ", "also ")

        # check if the text starts with a number
        if before_it_is_declared and (before_it_is_declared[0].isdigit() or before_it_is_declared[1].isdigit()):
            # print('~~~~~~~~~~~~~~~~~THIS IS A LIST~~~~~~~~~~~~~~~~~')
            # replace any \n with a space in case the text had a enter where a space should be
            clean = before_it_is_declared.replace(";\n", "\r")
            clean = clean.replace("\n", " ")
            # split by semi-colon
            peoples = clean.split("\r")
            for people in peoples:
                names = []
                people = people.strip()
                # print("PEWOPL: ", people)
                dirty_names = re.split(r'also\sknown\sas', people, flags=re.IGNORECASE)
                # print(dirty_names)
                name = dirty_names[0].strip().split(" ", 1)
                if len(name) > 1:
                    # print("name:", name[1])
                    name1 = name[1].strip()
                    # check if it still contains a number at the start
                    if name1[0].isdigit():
                        name1 = name1.split(" ", 1)
                        if len(name) > 1:
                            name1 = name1[1]
                    names.append(name1.strip())
                    # get the aliases
                    for alias in dirty_names[1:]:
                        cleaned_alias = re.sub(r'^\s*\d+[.)]\s*', '', alias, flags=re.MULTILINE)
                        names.append(cleaned_alias.strip().upper().replace('"', '').replace(".", "").replace("\t", ""))
                print(names)
                if names:
                    result.append(names)
        else:
            names = []
            # this is only one defendant
            clean = before_it_is_declared.replace("\n", " ")
            # print(clean)
            dirty_names = re.split(r'also\sknown\sas', clean, flags=re.IGNORECASE)
            for name in dirty_names:
                if name:
                    names.append(name.strip().upper().replace('"', '').replace(".", ""))
            print(names)
            if names:
                result.append(names)
    # print("---------------------END---------------------")

print(len(result))
# print(result)

df_dict = {'name': [], 'aliases': []}
for entity in result:
    # print("ENTITY", entity)
    df_dict['name'].append(entity[0])
    if len(entity) > 1:
        aliases = entity[1:]
    else:
        aliases = ['']
    df_dict['aliases'].append(';'.join(aliases))

df = pd.DataFrame(data=df_dict)
print(df)
df.to_excel('fiu_tt_court_order_names_20230707.xlsx')

