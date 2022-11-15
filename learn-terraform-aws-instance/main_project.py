
import os
import boto3
import json

contador = 0
dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : "", "aws_user_name" : "",
    "policy_name": "", "policy_description": "", "policy_action": [], "policy_effect": "", "policy_resource": ""}
nome_instancias = []


username = ""
region = ""
criou_user = False

global documento


def carrega_o_que_esta_no_json():
    documento = f'.auto-{region}.tfvars.json'
    with open(documento, 'r') as json_file:
        dict_variables = json.load(json_file)
    return dict_variables

def escreve_documento(dict_variables):
    documento = f'.auto-{region}.tfvars.json'
    json_object = json.dumps(dict_variables, indent = 4)
    with open(documento, 'w') as outfile:
        outfile.write(json_object)

def confere_resposta_nao_valida(resposta):
    if resposta == "y" or resposta == "Y" or resposta == "n" or resposta == "N":
        return False
    else:
        print("Você não digitou uma resposta válida. Tente novamente" + "\n")
        return True

def confere_se_eh_numero(resposta):
    if len(resposta) == 1:
        if resposta.isdigit():
            return False
    else:
        print("Você não digitou um número. Tente novamente" + "\n")
        return True


def manual_uso():
    print(""" 
    
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
    - Você deve colocar as credenciais do usuário no arquivo ~/.bashrc ou outro arquivo que carregue as variáveis de ambiente. Basta colocar as linhas abaixo no arquivo:
        export AWS_ACCESS_KEY_ID = SUA_ACCESS_KEY_ID"
        export AWS_SECRET_ACCESS_KEY = "SUA_SECRET_ACCESS_KEY"        
        E rodar o comando: source ~/.bashrc ou outro dependendo do arquivo em que você colocou as variáveis de ambiente.

    Observações sobre os manuseios dos recursos:
    - Você não pode deletar completamente o security group de uma instância. Dessa forma, caso você escolha essa opção, serão apagadas todas as regras (exceto a padrão que já vem na própria criação de instância na AWS).
    - As restrições que você irá aplicar ao usuário já são pré-definidas para facilitar a sua configuração.
    - Mudanças só serão feitas se você selecionar a opção aplicar mudanças.
    - Para acessar a senha do usuário e poder mexer no console da AWS vá para o documento file.txt criado, nele estará sua senha.
        Mas antes de acessar o file, pergunte para quem criou o programa a senha para descriptografar o arquivo (ela será pedida na tela). 

    EOF

    """)

    pronto = input("Digite qualquer tecla para continuar" + "\n")



def criar_restricoes():
    print("Ok, vamos começar então" + "\n")


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

    opcoes = input("""Você pode escolher entre as seguintes opções:

    1-  Descrever e listar recursos;
    2 - Descrever, listar e criar recursos;
    3 - Descrever, listar, criar e destruir recursos.

    Digite o número da opção que você deseja: """)   

    while confere_se_eh_numero(opcoes):
        opcoes = input("Digite o número da opção que você deseja: ")

    if opcoes == "1":
        dict_variables.update({"policy_name" : str("ReadOnlyAccess")})
        dict_variables.update({"policy_description" : str("Descrever e listar recursos")})
        dict_variables.update({"policy_action": list_describe["Action"]})
        dict_variables.update({"policy_effect": list_describe["Effect"]})
        dict_variables.update({"policy_resource": list_describe["Resource"]})
        escreve_documento(dict_variables)
    elif opcoes == "2":
        dict_variables.update({"policy_name" : str("ReadWriteAccess")})
        dict_variables.update({"policy_description" : str("Descrever, listar e criar recursos")})
        dict_variables.update({"policy_action": list_describe_create["Action"]})
        dict_variables.update({"policy_effect": list_describe_create["Effect"]})
        dict_variables.update({"policy_resource": list_describe_create["Resource"]})
        escreve_documento(dict_variables)
    elif opcoes == "3":
        dict_variables.update({"policy_name" : str("FullAccess")})
        dict_variables.update({"policy_description" : str("Descrever, listar, criar e destruir recursos")})
        dict_variables.update({"policy_action": list_describe_create_delete["Action"]})
        dict_variables.update({"policy_effect": list_describe_create_delete["Effect"]})
        dict_variables.update({"policy_resource": list_describe_create_delete["Resource"]})
        escreve_documento(dict_variables)

def criar_usuario():
    print("Então, pronto para começar a construir a infraestrutura? Vamos começar com o seu usuário a ser criado" + "\n")
    username = input("Digite o seu nome de usuário: ")
    print("\n")

    dict_variables.update({str("aws_user_name") : str(username)})
    escreve_documento(dict_variables)

    print("""Esse usuário criado já vem com as seguintes permissões: 
        - Criar e parar instâncias;
        - Alterar senha;
    """)

    criou_user = True

    criar_politicas = input("Você gostaria de criar outras restrições a esse usuário? (y/n)")

    while confere_resposta_nao_valida(criar_politicas):
        criar_politicas = input("Você gostaria de criar outras restrições a esse usuário? (y/n)")

    if criar_politicas == "y" or criar_politicas == "Y":
        criar_restricoes()
    elif criar_politicas == "n" or criar_politicas == "N":
        print("Ok, vamos continuar então" + "\n")


def info_basicas():
    print("Então, pronto para começar a construir a infraestrutura? Vamos apenas começar com um detalhe importante..." + "\n")


    global region
    region = input("Digite a região do projeto: ")
    print("\n")

    vpc_cidr_block = input("Digite o CIDR Block da VPC (como referência dois exemplos: us-east-1 tem como default o 10.0.0.0/16  e a us-west-2 tem como default 172.16.0.0/16): ")

    dict_variables.update({str("aws_region") : str(region)})
    dict_variables.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    escreve_documento(dict_variables)

def mudar_regiao():
    print("Você escolheu mudar de região. Vamos então atualizar as seguintes informações:" + "\n")
    global region 
    region = input("Digite a região do projeto: ")
    print("\n")

    vpc_cidr_block = input("Digite o CIDR Block da VPC (como referência dois exemplos: us-east-1 tem como default o 10.0.0.0/16  e a us-west-2 tem como default 172.16.0.0/16): ")

    global contador
    global dict_variables
    global nome_instancias
    contador = 0
    dict_variables = {"virtual_machines" : {},  "sec_groups" : {}, "sec_group_instances": {}, "aws_region" : "", "aws_user_name" : "",
    "policy_name": "", "policy_description": "", "policy_action": [], "policy_effect": "", "policy_resource": ""}
    nome_instancias = []


    dict_variables.update({str("aws_region") : str(region)})
    dict_variables.update({str("vpc_cidr_block") : str(vpc_cidr_block)})
    escreve_documento(dict_variables)


def cria_sec_group():
    null = None

    print("Vamos criar um grupo de segurança para a instância. Mas antes..." + "\n")

    qtd_sec_group = input("\n Quantos grupos de segurança você quer criar?" + "\n")

    for i in range(int(qtd_sec_group)):
        lista_group_name = []

        security_group_name = input("Digite o nome do grupo de segurança: ")
        print("\n")

        qtd_rules = input("Quantas regras você quer criar para esse grupo de segurança? ")

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
            description_security_group = input("Digite a descrição da regra do grupo de segurança: ")
            print("\n")
            aws_from_port = input("Digite a porta de origem: ")
            print("\n")
            aws_to_port = input("Digite a porta de destino: ")
            print("\n")
            aws_protocol = input("Digite o protocolo: ")
            print("\n")
            aws_cidr_blocks = input("Digite o bloco de ip: ")
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
            nome_inst_sec = input("Não menos importante, qual(ou quais) instância(s) você quer associar a esse grupo de segurança?")

            instancias = list(set(nome_inst_sec.split(",")))
            # eliminar repetição de instancias

            print(instancias)

            for i in range(len(instancias)):
                if instancias[i] not in nome_instancias:
                    print("Você não digitou um nome válido. Tente novamente" + "\n")
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

        # DEPOIS VÊ ISSO PARA COLOCAR O PADRÃO JUNTO E VER OS DESTROYS. DEPOIS PARTIR P OUTRAS REGIÕES
        # cria_sec_group_padrao()



def cria_sec_group_padrao():


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

        dict_variables["sec_group_instances"].update({str(nome_instancias[i]) : {"sec_names" : ["standard"]}})
        escreve_documento(dict_variables)



def create_instances():

    qtd_instancias = input("\n Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar?" + "\n")

    while confere_se_eh_numero(qtd_instancias):
        qtd_instancias = input("\n Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar?" + "\n")

    global contador

    for contador in range(int(qtd_instancias)):
        name_instance = input("""
        
        Digite o nome da instância: 
        
        R: """)
        
        nome_instancias.append(name_instance)

        image_id = input("""
        
        Digite o id da imagem a ser utilizada no servidor: 
        
        R: """)
        
        while True:
            instance_type_choice = input("""

            Agora você tem que escolher o tipo da instância a ser usada no servidor
            
            Você pode escolher dentre as seguintes: 
            1 - t2.micro;
            2 - t2.small;
            3 - t2.medium;
            4- t2.large
            
            R: """)

            if instance_type_choice == "1" or instance_type_choice == "2" or instance_type_choice == "3" or instance_type_choice == "4":
                break
            else:
                print("Você não digitou um tipo válido. Tente novamente" + "\n")
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

    sec_group = input("Você quer criar security groups com regras? (y/n)")

    while confere_resposta_nao_valida(sec_group):
        sec_group = input("Você quer criar um security group com regras? (y/n)")

    if sec_group == "y" or sec_group == "Y":
        cria_sec_group()
    elif sec_group == "n" or sec_group == "N":
        print("Ok, então o grupo de segurança vai ser padrão" + "\n")
        cria_sec_group_padrao()

        print("\n")

def lambda_handler_para(event, context, region):
    instances = [input("Agora digite o id da instância que você quer parar: ")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))


def lambda_handler_inicia(event, context, region):
    instances = [input("Agora digite o id da instância que você quer começar: ")]
    ec2 = boto3.client('ec2', region_name=region)
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))


def destruir_recurso():

    dict_variables = carrega_o_que_esta_no_json()

    destruir = input("""Qual recurso você gostaria de destruir:
    1- Instância;
    2- Grupo de sergurança;
    3- Usuário;
    4- Regra de um grupo de segurança
    
    R: """)

    if destruir == "1":
        instancia_destruir = input("""Você escolheu destruir uma instância.
        Digite o nome da instância que você quer destruir:
        R: """)

        inst_selecionada = dict_variables["virtual_machines"][instancia_destruir]

        destruir_yes_no = input(""" "Você está prestes a destruir a instância {instancia_destruir}: 
        
        {inst_selecionada} "\n"
        
        Você tem certeza que quer destruir a instância? (y/n) """)

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input("Você tem certeza que quer destruir a instância? (y/n)")

        if destruir_yes_no == "y" or "Y":
            print("Ok, destruindo a instância" + "\n")
            dict_variables["virtual_machines"].pop(str(instancia_destruir))

            # Se destruir instÂncia, destroi os security groups também?
            escreve_documento(dict_variables)
        elif destruir_yes_no == "n" or "N":
            print("Ok, então não destruiremos a instância" + "\n")

    elif destruir == "2":
        sec_group_destruir = input(""" Você escolheu destruir um grupo de segurança.
        Digite o nome do grupo de segurança que você quer destruir: 
        R: """)

        regras = str(dict_variables["sec_groups"][str(sec_group_destruir)])

        print(f'Você está prestes a destruir o grupo de segurança {sec_group_destruir}, que possui as seguintes regras: {regras} "\n" ')
        
        destruir_yes_no = input("""Você tem certeza que quer destruir o grupo de segurança? (y/n)
        R: """)

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input("Você tem certeza que quer destruir o grupo de segurança? Obs: destruir significa apagar todas as regras, EXCETO a padrão (y/n)")

        if destruir_yes_no == "y" or "Y":
            print("Ok, destruindo o grupo de segurança" + "\n")
            
            size = len(dict_variables["sec_groups"][str(sec_group_destruir)]["ingress"])
            while size > 1:
                if dict_variables["sec_groups"][str(sec_group_destruir)]["ingress"][size-1]["ingress"]["description"] != "Allow inbound traffic":
                    dict_variables["sec_groups"][str(sec_group_destruir)]["ingress"].pop()
                    size = size - 1
                    escreve_documento(dict_variables)

        elif destruir_yes_no == "n" or "N":
            print("Ok, então não destruiremos o grupo de segurança" + "\n")

    elif destruir == "3":
        user_destruir = input("""Você escolheu destruir um usuário. 
        Digite o nome do usuário que você quer destruir: """)

        destruir_yes_no = input("""Você está prestes a destruir o usuário {user_destruir} 
        
        Você tem certeza que quer destruir o usuário? (y/n) 
        R: """)

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input("Você tem certeza que quer destruir o usuário? (y/n)")

        if destruir_yes_no == "y" or "Y":
            print("Ok, destruindo o usuário" + "\n")
            dict_variables.pop("aws_user_name")
            escreve_documento(dict_variables)
        elif destruir_yes_no == "n" or "N":
            print("Ok, então não destruiremos o usuário" + "\n")

    elif destruir == "4":
        sec_group_destruir_regra = input("""Você escolheu destruir uma regra de um grupo de segurança. 
        Digite o nome do grupo de segurança que você quer destruir a regra: 
        R: """)

        regras = dict_variables["sec_groups"][str(sec_group_destruir_regra)]

        print(f'Você está prestes a destruir alguma regra do grupo de segurança {sec_group_destruir_regra}, que possui as seguintes regras:')


        for i in range(len(dict_variables["sec_groups"][str(sec_group_destruir_regra)]["ingress"])):
            # mostrar apenas description, protocol, from_port, to_port, cidr_blocks
            topico = dict_variables["sec_groups"][str(sec_group_destruir_regra)]["ingress"][i]["ingress"]

            print(f' {i} - {topico["description"]}, {topico["protocol"]}, {topico["from_port"]}, {topico["to_port"]}, {topico["cidr_blocks"]}')

        regra_destruir = input(f'Qual regra você quer destruir do grupo de segurança {sec_group_destruir_regra}? Digite o número da regra que você quer destruir:')


        destruir_yes_no = input("""
        Você tem certeza que quer destruir a regra {regra_destruir} do grupo de segurança? (y/n)
        R: """)

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input("Você tem certeza que quer destruir a regra {regra_destruir} do grupo de segurança? (y/n)")

        if destruir_yes_no == "y" or "Y":
            print("Ok, destruindo a regra do grupo de segurança" + "\n")
            dict_variables["sec_groups"][str(sec_group_destruir_regra)]["ingress"].pop(int(regra_destruir))
            escreve_documento(dict_variables)
        elif destruir_yes_no == "n" or "N":
            print("Ok, então não destruiremos a regra do grupo de segurança" + "\n")


def listar_recursos():
    print("Mas antes vamos garantir que o programa está atualizado... Aguarde um momento")

    refresh = os.popen("terraform refresh").read()

    escolha_listar = input("""Você quer listar:
    1- Instâncias e suas regiões;
    2- Grupos de segurança e suas regras;
    3- Usuários? """)

    while confere_se_eh_numero(escolha_listar):
        escolha_listar = input("Você quer listar: 1- Instâncias e suas regiões; 2- Grupos de segurança e suas regras; 3- Usuários? ")

    if escolha_listar == "1":
        print("Você escolheu listar instâncias e suas regiões" + "\n")
        os.system("terraform output nome_instancia_region")
        os.system("terraform output instances")
    elif escolha_listar == "2":
        print("Você escolheu listar grupos de segurança e suas regras" )
        os.system("terraform output sec_group_name")
    elif escolha_listar == "3":
        print("Você escolheu listar usuários" )
        os.system("terraform output aws_iam_users")


def aplicar_alteracoes():
    global documento
    documento = f'.auto-{region}.tfvars.json'

    os.system("source ~/.bashrc")

    os.system("terraform init")
    os.system(f'terraform terraform plan -var-file={documento}')
    os.system(f'terraform apply -var-file={documento}')

    if criou_user:
        os.system("terraform output password | base64 -d > test.txt")
        os.system("gpg --decrypt test.txt > file.txt")


def main():

    print("Olá caro usuário, seja bem vindo ao nosso projeto de automação de infraestrutura" + "\n")
    global region


    primeira_resposta = input("""Primeiramente, você gostaria de :
    
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
    
    R: """)


    if primeira_resposta == "0":
        print("Você escolheu manual de uso da aplicação" + "\n")
        manual_uso()
        main()
    elif primeira_resposta == "1":
        print("Você escolheu iniciar uma instância existente" + "\n")
        region = input("Digite a região da instância que você quer iniciar: ")
        lambda_handler_inicia(None, None, region)
        main()
    elif primeira_resposta == "2":
        print("Você escolheu parar uma instância existente" + "\n")
        region = input("Digite a região da instância que você quer parar: ")
        lambda_handler_para(None, None, region)
        main()
    elif primeira_resposta == "3":
        print("Você escolheu criar uma nova instância" + "\n")
        create_instances()
        main()
    elif primeira_resposta == "4":
        print("Você escolheu destruir algum recurso" + "\n")
        if region == "":
            info_basicas()
        destruir_recurso()
        main()
    elif primeira_resposta == "5":
        print("Você escolheu listar recursos" + "\n")
        if region == "":
            info_basicas()
        listar_recursos()
        main()
    elif primeira_resposta == "6":
        print("Você escolheu criar um usuário" + "\n")
        if region == "":
            info_basicas()
        criar_usuario()
        main()
    elif primeira_resposta == "7":
        print("Você escolheu aplicar todas alterações feitas nessa região {region}" + "\n")
        aplicar_alteracoes()
        main()
    elif primeira_resposta == "8":
        mudar_regiao()
        main()
    elif primeira_resposta == "9":
        print("Você escolheu sair do programa" + "\n")
        print("Obrigado por usar o nosso programa, volte sempre!" + "\n")
        return




# Executa a função main
main()
# criar_usuario()





# os.system("terraform output password | base64 -d > test.txt")

# os.system("gpg --decrypt test.txt > file.txt")

# region_global = "us-east-1"
