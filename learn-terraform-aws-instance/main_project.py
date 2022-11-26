
import os
import boto3
import json

dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : ""}
dict_users = {"aws_user_name" : []}
nome_instancias = []
username = ""
region = ""

global documento

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def carrega_o_que_esta_no_json():
    documento = f'terraform-{region}/.auto-{region}.tfvars.json'
    with open(documento, 'r') as json_file:
        dict_variables = json.load(json_file)
    return dict_variables

def carrega_o_que_esta_no_json_users():
    file = 'terraform-users/.auto.tfvars.json'
    with open(file, 'r') as json_file:
        dict_users = json.load(json_file)
    return dict_users

def escreve_documento(dict_variables):
    documento = f'terraform-{region}/.auto-{region}.tfvars.json'
    json_object = json.dumps(dict_variables, indent = 4)
    with open(documento, 'w') as outfile:
        outfile.write(json_object)

def escreve_usuario(dict_users):
    file = 'terraform-users/.auto.tfvars.json'
    json_object = json.dumps(dict_users, indent = 4)
    with open(file, 'w') as outfile:
        outfile.write(json_object)


def confere_resposta_nao_valida(resposta):
    if resposta == "y" or resposta == "Y" or resposta == "n" or resposta == "N":
        return False
    else:
        print(f"{bcolors.FAIL}Você não digitou uma resposta válida. Tente novamente {bcolors.ENDC}" + "\n")
        return True

def confere_se_eh_numero(resposta):
    if len(resposta) == 1:
        if resposta.isdigit():
            return False
    else:
        print(f"{bcolors.FAIL}Você não digitou um número. Tente novamente {bcolors.ENDC}" + "\n")
        return True


def manual_uso():
    print(f"""{bcolors.OKCYAN} 
    
===================================================================================================

Bem-vindo ao manual de uso da aplicação de criação de recursos na AWS.

===================================================================================================

    A aplicação foi desenvolvida para facilitar a criação de instâncias na AWS, com a possibilidade de criar
    instâncias com diferentes configurações de segurança (grupos de segurança) que possuem diferentes regras.

Dessa forma, você poderá:
    - Criar instâncias com nome, imagem da máquina, tipo de host.
    - Criar grupos de segurança e associar a essas máquinas.
    - Criar regras de segurança para os grupos de segurança.
    - Criar um usuário com permissões de acesso a recursos da AWS.
    - Listar os recursos criados, como instâncias, grupos de segurança e suas regras e usuários.
    - Deletar instâncias, grupos de segurança, regras de grupo de segurança, e usuário (o que você criou).

Observação para esta aplicação : 
    - Você deve ter instalado o Python 3.8.5 ou superior.
    - Você deve ter instalado o Terraform 0.14.5 ou superior.
    - Você deve ter instalado o AWS CLI 2.1.19 ou superior.
    - Você deve ter instalado o Boto3 1.17.19 ou superior.
    - Você deve ter instalado o JSON 2.0.9 ou superior.
    - Você deve ter instalado o OS 1.0.1 ou superior.

Observações de uso da aplicação:
    - Você deve ter uma conta na AWS.
    - Você deve ter um usuário com permissões de acesso a recursos da AWS.
    - Você deve colocar as credenciais do usuário no arquivo ~/.bashrc ou outro arquivo que carregue as variáveis de ambiente. 
        Basta colocar as linhas abaixo no arquivo:
            export AWS_ACCESS_KEY_ID = SUA_ACCESS_KEY_ID"
            export AWS_SECRET_ACCESS_KEY = "SUA_SECRET_ACCESS_KEY"        
            E rodar o comando: source ~/.bashrc ou outro dependendo do arquivo em que você colocou as variáveis de ambiente.

    Observações sobre os manuseios dos recursos:
    - Você não pode deletar completamente o security group de uma instância. Dessa forma, caso você escolha essa opção, serão 
      apagadas todas as regras (exceto a padrão que já vem na própria criação de instância na AWS).
    - As restrições que você irá aplicar ao usuário já são pré-definidas para facilitar a sua configuração.
    - Mudanças só serão feitas se você selecionar a opção aplicar mudanças.
    - Para acessar a senha do usuário e poder mexer no console da AWS, primeiro você terá que selecionar a opção para aplicar as mudanças e depois
      de aplicadas, como output do programa você terá as informações sobre os usuários criados, o que inclue as senhas de 10 dígitos.

    EOF

    {bcolors.ENDC}""")

    pronto = input(f"{bcolors.OKGREEN}Digite qualquer tecla para continuar" + "\n")



def criar_restricoes():
    global dict_users

    print(f"{bcolors.OKCYAN}Ok, vamos começar então {bcolors.ENDC}" + "\n")

    list_describe = {
            "Action": [
            "ec2:Describe*",
            "ec2:Get*"
            ],
            "Effect": "Allow",
            "Resource": "*"
        }


    list_describe_create =  {
        "Action": [
            "ec2:Describe*",
            "ec2:Get*",
            "ec2:Create*",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:ModifySecurityGroupRules",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:AuthorizeSecurityGroupIngress", 
            "ec2:RevokeSecurityGroupIngress", 
            "ec2:AuthorizeSecurityGroupEgress", 
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RunInstances"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }

    list_describe_create_delete = {
        "Action": [
            "ec2:Describe*",
            "ec2:Get*",
            "ec2:Create*",
            "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
            "ec2:ModifySecurityGroupRules",
            "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
            "ec2:AuthorizeSecurityGroupIngress", 
            "ec2:RevokeSecurityGroupIngress", 
            "ec2:AuthorizeSecurityGroupEgress", 
            "ec2:RevokeSecurityGroupEgress",
            "ec2:RunInstances",
            "ec2:TerminateInstances",
            "ec2:Delete*"
        ],
        "Effect": "Allow",
        "Resource": "*"
        }

    opcoes = input(f""" {bcolors.OKCYAN}
    
    Para facilitar sua vida, você pode escolher entre as seguintes opções:

        1-  Descrever e listar recursos;
        2 - Descrever, listar e criar recursos;
        3 - Descrever, listar, criar e destruir recursos.

    Digite o número da opção que você deseja: {bcolors.ENDC}""")   

    while confere_se_eh_numero(opcoes):
        print("\n")
        opcoes = input(f"{bcolors.OKCYAN} Digite o número da opção que você deseja: {bcolors.ENDC}")

    if opcoes == "1":
        dict_users["aws_user_name"].append({"username" : username, "policy_name": "ReadOnlyAccess_" + username, "policy_description": "Descrever e listar recursos", 
            "policy_action": list_describe["Action"], "policy_resource": list_describe["Resource"], "policy_effect": list_describe["Effect"]})
        escreve_usuario(dict_users)
    elif opcoes == "2":
        dict_users["aws_user_name"].append({"username" : username, "policy_name": "ReadWriteAccess_" + username, "policy_description": "Descrever, listar e criar recursos", 
            "policy_action": list_describe_create["Action"], "policy_resource": list_describe_create["Resource"], "policy_effect": list_describe_create["Effect"] })
        escreve_usuario(dict_users)
    elif opcoes == "3":
        dict_users["aws_user_name"].append({"username" : username, "policy_name": "ReadWriteDeleteAccess_" + username, "policy_description": "Descrever, listar, criar e destruir recursos", 
            "policy_action": list_describe_create_delete["Action"], "policy_resource": list_describe_create_delete["Resource"], "policy_effect": list_describe_create_delete["Effect"] })
        escreve_usuario(dict_users)


    # os.system(f'cd terraform-users && terraform init && terraform  plan && terraform apply')


def criar_usuario():
    print(f"{bcolors.OKCYAN}Então, pronto para começar a construir a infraestrutura? Vamos começar com o seu usuário a ser criado {bcolors.ENDC}" + "\n")
    global username
    global dict_users
    username = input(f"{bcolors.OKCYAN}Digite o seu nome de usuário: {bcolors.ENDC}")
    print("\n")


    print(f"""
    {bcolors.OKCYAN}
    Esse usuário criado já vem com as seguintes permissões: 
        - Criar e parar instâncias;
        - Alterar senha;
    {bcolors.ENDC}""")

    print("\n")
    criar_politicas = input(f"{bcolors.OKCYAN}Você gostaria de criar restrições a esse usuário? (y/n). Se resposta for n, ele terá todas as permissões {bcolors.ENDC}")

    while confere_resposta_nao_valida(criar_politicas):
        criar_politicas = input(f"{bcolors.OKCYAN}Você gostaria de criar restrições a esse usuário? (y/n). Se resposta for n, ele terá todas as permissões. {bcolors.ENDC}")

    if criar_politicas == "y" or criar_politicas == "Y":
        criar_restricoes()
    elif criar_politicas == "n" or criar_politicas == "N":
        dict_users["aws_user_name"].append({"username": username, "policy_name": "FullAccess_" + username, "policy_description": "Usuario possui acesso a tudo", "policy_action": ["*"], "policy_resource": "*", "policy_effect": "Allow"})
        escreve_usuario(dict_users)
        print(f"{bcolors.OKGREEN} Ok, vamos continuar então {bcolors.ENDC}" + "\n")
        
        # os.system(f'cd terraform-users && terraform init && terraform  plan && terraform apply')

def info_basicas():
    global region
    global dict_variables
    global dict_users
    global nome_instancias
    global documento

    print(f"{bcolors.OKCYAN}Então, pronto para começar a construir a infraestrutura? Vamos apenas começar com um detalhe importante... {bcolors.ENDC} \n ")

    resposta = input(f"{bcolors.OKCYAN}Em qual região você vai construir sua infraestrutura? [1 - us-east-1 ou 2- us-west-1]?")
    print("\n")

    while True:
        if resposta == "1" or resposta == "2":
            break
        else:
            resposta = input(f"{bcolors.FAIL}Resposta inválida. Em qual região você vai construir sua infraestrutura? [1 - us-east-1 ou 2- us-west-1]? {bcolors.ENDC}")


    if resposta == "1":
        region = "us-east-1"
    elif resposta == "2":
        region = "us-west-1"

    if region == "us-east-1":
        vpc_cidr_block = "10.0.0.0/16"
    else:
        vpc_cidr_block = "172.16.0.0/16" 


    documento = f'terraform-{region}/.auto-{region}.tfvars.json'


    if os.path.exists(documento):
        dict_variables = carrega_o_que_esta_no_json()
        dict_users = carrega_o_que_esta_no_json_users()
        nome_instancias = [instance for instance in {key for key in dict_variables["virtual_machines"]}]
    else:
        dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : "", "vpc_cidr_block":""}
        dict_users = {"aws_user_name" : []}
        nome_instancias = []


    dict_variables.update({str("aws_region") : str(region)})
    dict_variables.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    escreve_documento(dict_variables)


def mudar_regiao():
    global region 
    global dict_variables
    global dict_users
    global nome_instancias
    global documento

    print(f"{bcolors.OKCYAN} Você escolheu mudar de região. Vamos então atualizar as seguintes informações: {bcolors.ENDC}" + "\n")
    resposta = input(f"{bcolors.OKCYAN} Em qual região você vai construir sua infraestrutura? Digite o número da região desejada [1 - us-east-1 ou 2- us-west-1]? {bcolors.ENDC}")
    print("\n")

    while True:
        if resposta == "1" or resposta == "2":
            break
        else:
            resposta = input(f"{bcolors.OKCYAN}Em qual região você vai construir sua infraestrutura? Digite o número da região desejada [1 - us-east-1 ou 2- us-west-1]? {bcolors.ENDC}")


    if resposta == "1":
        region = "us-east-1"
    elif resposta == "2":
        region = "us-west-1"

    if region == "us-east-1":
        vpc_cidr_block = "10.0.0.0/16"
    else:
        vpc_cidr_block = "172.16.0.0/16" 

    documento = f'terraform-{region}/.auto-{region}.tfvars.json'

    dict_antigo = dict_variables

    if os.path.exists(documento):
        dict_variables = carrega_o_que_esta_no_json()
        dict_users = carrega_o_que_esta_no_json_users()
    else:
        dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : []}
        dict_users = {"aws_user_name" : []}
        nome_instancias = []


    dict_variables.update({str("aws_region") : str(region)})
    dict_variables.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    escreve_documento(dict_variables)



def cria_sec_group():
    null = None

    print(f"{bcolors.OKCYAN}Vamos criar um grupo de segurança para a instância. Mas antes... {bcolors.ENDC}" + "\n")

    qtd_sec_group = input(f" {bcolors.OKCYAN} Quantos grupos de segurança você quer criar? {bcolors.ENDC}" + "\n")

    for i in range(int(qtd_sec_group)):
        lista_group_name = []

        security_group_name = input(f"{bcolors.OKCYAN}Digite o nome do grupo de segurança número {i}: {bcolors.ENDC}")
        print("\n")

        qtd_rules = input(f"{bcolors.OKCYAN}Quantas regras você quer criar para esse grupo de segurança? {bcolors.ENDC}" + "\n")

        dict_standard_rule = {"ingress" : {"description" : "Allow inbound traffic", \
                            "from_port" : 0, \
                            "to_port" : 0, \
                            "protocol" : -1, \
                            "ipv6_cidr_blocks" : null, \
                            "prefix_list_ids" : null, \
                            "self" : null , \
                            "security_groups" : null , \
                            "cidr_blocks" : ["0.0.0.0/0"]}}

        lista_regras = [dict_standard_rule]

        for i in range(int(qtd_rules)):
            description_security_group = input(f"{bcolors.OKCYAN}Digite a descrição da regra do grupo de segurança número {i}: {bcolors.ENDC}")
            print("\n")
            aws_from_port = input(f"{bcolors.OKCYAN}Digite a porta de origem R:{bcolors.ENDC}")
            print("\n")
            aws_to_port = input(f"{bcolors.OKCYAN}Digite a porta de destino R:{bcolors.ENDC}")
            print("\n")
            aws_protocol = input(f"{bcolors.OKCYAN}Digite o protocolo R:{bcolors.ENDC}")
            print("\n")
            aws_cidr_blocks = input(f"{bcolors.OKCYAN}Digite o bloco CIDR R: {bcolors.ENDC}")
            print("\n")

            dict_rules = {"ingress" : {"description" : str(description_security_group), \
                                        "from_port" : str(aws_from_port), 
                                        "to_port" : str(aws_to_port), \
                                        "protocol" : str(aws_protocol), 
                                        "ipv6_cidr_blocks" : null,  \
                                        "prefix_list_ids" : null,  \
                                        "self" : null,  \
                                        "security_groups" : null,  \
                                        "cidr_blocks" : [str(aws_cidr_blocks)]}}
            
            lista_regras.append(dict_rules)

            dict_variables["sec_groups"].update({str(security_group_name) : {"name" : security_group_name, "ingress": lista_regras}})
            escreve_documento(dict_variables)

        flag = True
        while flag:
            nome_inst_sec = input(f"{bcolors.OKCYAN} Não menos importante, qual(ou quais) instância(s) você quer associar a esse grupo de segurança? Dê a sua resposta com vírgula, exemplo: vm1,vm2.  R:{bcolors.ENDC}")

            instancias = list(set(nome_inst_sec.split(",")))

            for i in range(len(instancias)):
                if instancias[i] not in nome_instancias:
                    print(f"{bcolors.FAIL}Você não digitou um nome válido. Tente novamente {bcolors.ENDC}" + "\n")
                else:
                    if i == len(instancias)-1:
                        flag = False

        for nome_inst_sec_group in instancias:
            if nome_inst_sec_group in dict_variables["sec_group_instances"]:
                lista_group_name = dict_variables["sec_group_instances"][nome_inst_sec_group]["sec_names"]
                lista_group_name.append(security_group_name)
                dict_variables["sec_group_instances"].update({nome_inst_sec_group : {"sec_names" : lista_group_name}})
            else:
                dict_variables["sec_group_instances"].update({str(nome_inst_sec_group) : {"sec_names" : [str(security_group_name)]}})

        escreve_documento(dict_variables)

def cria_sec_group_padrao(name_instance):


    lista_regras = []

    null = None

    dict_rules = {"ingress" : {"description" : "Allow inbound traffic", \
                                "from_port" : 0, \
                                "to_port" : 0, \
                                "protocol" : -1, \
                                "ipv6_cidr_blocks" : null, \
                                "prefix_list_ids" : null, \
                                "self" : null , \
                                "security_groups" : null , \
                                "cidr_blocks" : ["0.0.0.0/0"]}}
            
    lista_regras.append(dict_rules)

    dict_variables["sec_groups"].update({"standard" : {"name" : "standard", "ingress": lista_regras}})
    escreve_documento(dict_variables)


    for i in range(len(nome_instancias)):
        if nome_instancias[i] == name_instance:
            dict_variables["sec_group_instances"].update({str(nome_instancias[i]) : {"sec_names" : ["standard"]}})
            escreve_documento(dict_variables)


def criar_instancias():
    global region

    qtd_instancias = input(f"\n {bcolors.OKCYAN}Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar? {bcolors.ENDC}" + "\n")

    while confere_se_eh_numero(qtd_instancias):
        qtd_instancias = input(f"\n {bcolors.FAIL} Resposta inválida. Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar? {bcolors.ENDC}" + "\n")

    for i in range(int(qtd_instancias)):
        name_instance = input(f"""{bcolors.OKCYAN}
        
    Digite o nome da instância: 
        
    R: {bcolors.ENDC}""")
        
        nome_instancias.append(name_instance)

        image_id_resposta = input(f""" {bcolors.OKCYAN}
        
    Qual imagem você quer utilizar na instância? [1 - Ubuntu Server 20.04 LTS ou 2 - Ubuntu Server 22.04 LTS]
        
    R: {bcolors.ENDC}""")

        if image_id_resposta == "1" and region == "us-east-1":
            image_id = "ami-0149b2da6ceec4bb0"
        elif image_id_resposta == "2" and region == "us-east-1":
            image_id = "ami-08c40ec9ead489470"
        elif image_id_resposta == "1" and region == "us-west-1":
            image_id = "ami-03f6d497fceb40069"
        elif image_id_resposta == "2" and region == "us-west-1":
            image_id = "ami-02ea247e531eb3ce6"
        
        
        while True:
            instance_type_choice = input(f"""{bcolors.OKCYAN}

        Agora você tem que escolher o tipo da instância a ser usada no servidor
            
        Você pode escolher dentre as seguintes: 
            1 - t2.micro;
            2 - t2.small;
            3 - t2.medium;
            4- t2.large
            
            R: {bcolors.ENDC}""")

            if instance_type_choice == "1" or instance_type_choice == "2" or instance_type_choice == "3" or instance_type_choice == "4":
                break
            else:
                print(f"{bcolors.FAIL}Você não digitou um tipo válido. Tente novamente {bcolors.ENDC}" + "\n")
        # instance_type_choice = input("\n  Você pode escolher dentre as seguintes: [1 - t2.micro, 2 - t2.small, 3 - t2.medium, 4- t2.large]?")
        if instance_type_choice == "1":
            instance_type = "t2.micro"
        elif instance_type_choice == "2":
            instance_type = "t2.small"
        elif instance_type_choice == "3":
            instance_type = "t2.medium"
        elif instance_type_choice == "4":
            instance_type = "t2.large"

        dict_variables["virtual_machines"].update({str(name_instance) : {"image_id" : str(image_id), "instance_type" : str(instance_type)}})
        escreve_documento(dict_variables)   

    sec_group = input(f"{bcolors.OKCYAN} Você quer criar security groups com regras? (y/n) {bcolors.ENDC}" + "\n")

    while confere_resposta_nao_valida(sec_group):
        sec_group = input(f"{bcolors.OKCYAN}Você quer criar um security group com regras? (y/n) {bcolors.ENDC} \n")

    if sec_group == "y" or sec_group == "Y":
        cria_sec_group()
    elif sec_group == "n" or sec_group == "N":
        print(f"{bcolors.OKCYAN} Ok, então o grupo de segurança vai ser padrão {bcolors.ENDC}" + "\n")
        cria_sec_group_padrao(name_instance)

        print("\n")

def lambda_handler_para(event, context, region):
    instances = [input("Agora digite o id da instância que você quer parar: ")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))


def lambda_handler_inicia(event, context, region):
    instances = [input(f"{bcolors.OKGREEN}Agora digite o id da instância que você quer começar: {bcolors.ENDC}")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))


def destruir_recurso():

    dict_variables = carrega_o_que_esta_no_json()

    destruir = input(f"""{bcolors.OKCYAN}
    Qual recurso você gostaria de destruir:

    1- Instância;
    2- Grupo de segurança;
    3- Usuário;
    4- Regra de um grupo de segurança
    
    R: {bcolors.ENDC}""")

    if destruir == "1":
        instancia_destruir = input(f"""{bcolors.OKCYAN}
    Você escolheu destruir uma instância.
    Digite o nome da instância que você quer destruir:
    R: {bcolors.ENDC}""")
        print("\n")

        inst_selecionada = dict_variables["virtual_machines"][instancia_destruir]

        destruir_yes_no = input(f'{bcolors.WARNING}Você está prestes a destruir a instância {instancia_destruir}: {inst_selecionada} \n .Você tem certeza que quer destruir a instância? (y/n) {bcolors.ENDC}')

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input(f"{bcolors.WARNING}Você tem certeza que quer destruir a instância? (y/n) \n {bcolors.ENDC}")

        if destruir_yes_no == "y" or destruir_yes_no == "Y":
            print("\n")
            print(f"{bcolors.OKGREEN}Ok, destruindo a instância  {bcolors.ENDC}" + "\n")
            dict_variables["virtual_machines"].pop(str(instancia_destruir))
            for chave in dict_variables["sec_group_instances"].copy():
                if instancia_destruir == chave:
                    del dict_variables["sec_group_instances"][str(instancia_destruir)]

            escreve_documento(dict_variables)
        elif destruir_yes_no == "n" or destruir_yes_no == "N":
            print("\n")
            print(f"{bcolors.FAIL}Ok, então não destruiremos a instância {bcolors.FAIL}" + "\n")

    elif destruir == "2":
        sec_group_destruir = input(f"""{bcolors.OKCYAN}
    Você escolheu destruir um grupo de segurança.
    Digite o nome do grupo de segurança que você quer destruir: 
    R: {bcolors.ENDC}""")

        regras = str(dict_variables["sec_groups"][str(sec_group_destruir)])

        print(f'{bcolors.WARNING}Você está prestes a destruir o grupo de segurança {sec_group_destruir}, que possui as seguintes regras: {regras} {bcolors.ENDC}"\n" ')
        
        destruir_yes_no = input(f"{bcolors.WARNING}Você tem certeza que quer destruir o grupo de segurança? Obs: destruir significa apagar todas as regras, EXCETO a padrão (y/n) R: {bcolors.ENDC}")

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input(f"{bcolors.WARNING}Você tem certeza que quer destruir o grupo de segurança? Obs: destruir significa apagar todas as regras, EXCETO a padrão (y/n) R: {bcolors.ENDC}")

        if destruir_yes_no == "y" or destruir_yes_no == "Y":
            print("\n")
            print(f"{bcolors.OKGREEN}Ok, destruindo o grupo de segurança {bcolors.ENDC}" + "\n")
            
            size = len(dict_variables["sec_groups"][str(sec_group_destruir)]["ingress"])
            while size > 1:
                if dict_variables["sec_groups"][str(sec_group_destruir)]["ingress"][size-1]["ingress"]["description"] != "Allow inbound traffic":
                    dict_variables["sec_groups"][str(sec_group_destruir)]["ingress"].pop()
                    size = size - 1
                    escreve_documento(dict_variables)

        elif destruir_yes_no == "n" or destruir_yes_no == "N":
            print("\n")
            print(f"{bcolors.FAIL}Ok, então não destruiremos o grupo de segurança {bcolors.ENDC}" + "\n")

    elif destruir == "3":
        user_destruir = input(f""" {bcolors.OKCYAN}
    Você escolheu destruir um usuário. 
    Digite o nome do usuário que você quer destruir R: {bcolors.ENDC}""")


        destruir_yes_no = input(f'{bcolors.WARNING}Você está prestes a destruir o usuário {user_destruir}. Você tem certeza que quer destruir o usuário? (y/n). \n R: {bcolors.ENDC}')

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input(f"{bcolors.WARNING}Você tem certeza que quer destruir o usuário? (y/n) {bcolors.ENDC}")

        if destruir_yes_no == "y" or destruir_yes_no == "Y":
            print("\n")
            print(f"{bcolors.OKGREEN }Ok, destruindo o usuário {bcolors.ENDC}" + "\n")
            size = len(dict_users["aws_user_name"])
            for i in range(size):
                if dict_users["aws_user_name"][i]["username"] == user_destruir:
                    dict_users["aws_user_name"].pop(i)
                    size = size - 1
                    escreve_usuario(dict_users)
                    # os.system(f'cd terraform-users && terraform init && terraform  plan && terraform apply')
                    break

        elif destruir_yes_no == "n" or destruir_yes_no == "N":
            print("\n")
            print(f"{bcolors.FAIL}Ok, então não destruiremos o usuário {bcolors.ENDC}" + "\n")

    elif destruir == "4":
        sec_group_destruir_regra = input(f"""{bcolors.OKCYAN}
    Você escolheu destruir uma regra de um grupo de segurança. 
    Digite o nome do grupo de segurança que você quer destruir a regra: 
    R: {bcolors.ENDC}""")

        regras = dict_variables["sec_groups"][str(sec_group_destruir_regra)]

        print(f'{bcolors.WARNING}Você está prestes a destruir alguma regra do grupo de segurança {sec_group_destruir_regra}, que possui as seguintes regras : {bcolors.ENDC} \n')


        for i in range(len(dict_variables["sec_groups"][str(sec_group_destruir_regra)]["ingress"])):
            topico = dict_variables["sec_groups"][str(sec_group_destruir_regra)]["ingress"][i]["ingress"]
            print(f' {bcolors.WARNING} {i} - {topico["description"]}, {topico["protocol"]}, {topico["from_port"]}, {topico["to_port"]}, {topico["cidr_blocks"]} {bcolors.ENDC}')

        print("\n")
        regra_destruir = input(f'{bcolors.OKCYAN}Qual regra você quer destruir do grupo de segurança {sec_group_destruir_regra}? Digite o número da regra que você quer destruir R: \n {bcolors.ENDC}')


        destruir_yes_no = input(f"""{bcolors.WARNING}
    Você tem certeza que quer destruir a regra {regra_destruir} do grupo de segurança? (y/n)
    R: {bcolors.ENDC}""")

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input(f"{bcolors.WARNING}Você tem certeza que quer destruir a regra {regra_destruir} do grupo de segurança? (y/n) {bcolors.ENDC}")

        if destruir_yes_no == "y" or destruir_yes_no == "Y":
            print("\n")
            print(f"{bcolors.OKGREEN}Ok, destruindo a regra do grupo de segurança {bcolors.ENDC}" + "\n")
            dict_variables["sec_groups"][str(sec_group_destruir_regra)]["ingress"].pop(int(regra_destruir))
            escreve_documento(dict_variables)
        elif destruir_yes_no == "n" or destruir_yes_no == "N":
            print("\n")
            print(f"{bcolors.FAIL}Ok, então não destruiremos a regra do grupo de segurança {bcolors.ENDC}" + "\n")


def listar_recursos():
    global region

    session = boto3.Session(profile_name='default', region_name=region)
    ec2client = session.client('ec2')
    ec2iam = session.client('iam')
    ec2re = session.resource('ec2')


    escolha_listar = input(f""" {bcolors.OKCYAN}
    Você quer listar:
        1- Instâncias e suas regiões;
        2- Grupos de segurança e suas regras;
        3- Usuários? 
        R : {bcolors.ENDC}""")

    while confere_se_eh_numero(escolha_listar):
        escolha_listar = input(f""" {bcolors.OKCYAN}
    Você quer listar: 
        1- Instâncias e suas regiões; 
        2- Grupos de segurança e suas regras; 
        3- Usuários? {bcolors.ENDC}""")

    if escolha_listar == "1":
        print("\n")
        print(f"{bcolors.OKCYAN}Você escolheu listar instâncias e suas regiões {bcolors.ENDC}" + "\n")

        for each in ec2re.instances.all():
            print(f"{bcolors.OKGREEN} Id: " + each.id + " " + "| Nome: " + each.tags[0]["Value"] + " " + "| Estado: " + each.state["Name"] + " " +
            "| Tipo: " + each.instance_type +  "| Região: "+  each.placement['AvailabilityZone'] + "\n " + f"{bcolors.ENDC}")


    elif escolha_listar == "2":
        print("\n")
        print(f"{bcolors.OKCYAN}Você escolheu listar grupos de segurança e suas regras {bcolors.ENDC}" )
        for each in ec2re.security_groups.all():
            print(f"{bcolors.OKGREEN}Nome: " + each.group_name + "\n")
            for rule in each.ip_permissions:
                print(f"{bcolors.OKGREEN}Regra: " + str(rule) + "\n")
                print(f"================================================================================================= {bcolors.ENDC}")
         

    elif escolha_listar == "3":
        print("\n")
        print(f"{bcolors.OKCYAN}Você escolheu listar usuários {bcolors.ENDC}" )
        for user in ec2iam.list_users()['Users']:
            print(f"{bcolors.OKGREEN}")
            print("Usuário: {0}\ID: {1}\nARN: {2}\Criado em: {3}\n".format(
                user['UserName'],
                user['UserId'],
                user['Arn'],
                user['CreateDate']
                )
            )
            print(f"{bcolors.ENDC}")

def aplicar_alteracoes():
    global documento
    documento = f'.auto-{region}.tfvars.json'

    print(f"{bcolors.OKGREEN} Aplicando as mudanças feitas até aqui na região atual : {region} {bcolors.ENDC}" + "\n")

    os.system("source ~/.bashrc")

    os.system(f'cd terraform-users && terraform init && terraform  plan && terraform apply')

    os.system(f'cd terraform-{region} && terraform init && terraform  plan -var-file={documento} && terraform apply -var-file={documento}')


def main():

    print("\n")
    print(f"{bcolors.OKCYAN}{bcolors.BOLD}Olá caro usuário, seja bem vindo ao nosso projeto de automação de infraestrutura {bcolors.ENDC}" + "\n")

    info_basicas()

    global region
    global dict_users
    escreve_usuario(dict_users)

    programa_on = True
    while programa_on:
        primeira_resposta = input(f"""{bcolors.OKCYAN}Primeiramente, você gostaria de :
        
        0 - Manual de uso da aplicação; 
        1 - Iniciar uma instância existente;
        2 - Parar uma instância existente;
        3 - Criar uma nova instância e security groups;
        4 - Destruir algum recurso;
        5 - Listar recursos;
        6 - Criar um usuário; 
        7 - Aplicar todas alterações feitas em uma região;
        8 - Mudar a região onde você está trabalhando;
        9 - Sair do programa
        
        R: {bcolors.ENDC}""")


        if primeira_resposta == "0":
            print(f"{bcolors.OKCYAN}Você escolheu manual de uso da aplicação {bcolors.ENDC}" + "\n")
            manual_uso()
        elif primeira_resposta == "1":
            print(f"{bcolors.OKCYAN}Você escolheu iniciar uma instância existente {bcolors.ENDC}" + "\n")
            region = input(f"{bcolors.OKGREEN}Digite a região da instância que você quer iniciar: {bcolors.ENDC}")
            lambda_handler_inicia(None, None, region)
        elif primeira_resposta == "2":
            print(f"{bcolors.OKCYAN}Você escolheu parar uma instância existente {bcolors.ENDC}" + "\n")
            region = input(f"{bcolors.OKGREEN}Digite a região da instância que você quer parar: {bcolors.ENDC}")
            lambda_handler_para(None, None, region)
        elif primeira_resposta == "3":
            print(f"{bcolors.OKCYAN}Você escolheu criar uma nova instância {bcolors.ENDC}" + "\n")
            criar_instancias()
        elif primeira_resposta == "4":
            print(f"{bcolors.OKCYAN}Você escolheu destruir algum recurso {bcolors.ENDC}" + "\n")
            destruir_recurso()
        elif primeira_resposta == "5":
            print(f"{bcolors.OKCYAN}Você escolheu listar recursos {bcolors.ENDC}" + "\n")
            listar_recursos()
        elif primeira_resposta == "6":
            print(f"{bcolors.OKCYAN}Você escolheu criar um usuário {bcolors.ENDC}" + "\n")
            criar_usuario()
        elif primeira_resposta == "7":
            print(f"{bcolors.OKCYAN}Você escolheu aplicar todas alterações feitas nessa região {region} {bcolors.ENDC}" + "\n")
            aplicar_alteracoes()
        elif primeira_resposta == "8":
            mudar_regiao()
        elif primeira_resposta == "9":
            print(f"{bcolors.OKCYAN}Você escolheu sair do programa" + "\n")
            print(f"Obrigado por usar o nosso programa, volte sempre!{bcolors.ENDC}" + "\n")
            programa_on = False
            return



main()

