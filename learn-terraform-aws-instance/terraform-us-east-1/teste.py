import os

# salvar resultado do comando em uma variável
# result = os.popen("terraform output aws_iam_users").read()

# print("ESSES SÂO OS USERS: ", result)

import json 

region = input("Regiao: ")

documento = f'.auto-{region}.tfvars.json'

print(documento)

# colocar o nome da regiao ao lado do valor teste do dicionario
dict_variables = {
    "teste": region
}

dict_variables = {"teste" : "teste" + region}

def escreve_documento(dict_variables):
    json_object = json.dumps(dict_variables, indent = 4)
    with open(documento, 'w') as outfile:
        outfile.write(json_object)

escreve_documento(dict_variables)