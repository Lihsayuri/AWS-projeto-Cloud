
import os
import boto3
import json

contador = 0
dict_variables = {"virtual_machines" : {},  "sg_ingress_rules" : {}}
nome_instancias = []

username = ""
region = ""



def escreve_documento(dict_variables):
    json_object = json.dumps(dict_variables, indent = 4)
    with open('.auto.tfvars.json', 'w') as outfile:
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

def criar_restricoes():
    qtd_policas = input("Quantas restrições você quer criar?")

    for i in range(int(qtd_policas)):
        nome_policia = input("Digite o nome da restrição: ")
        print("\n")
        aws_action = input("Digite a ação que você quer restringir: ")
        print("\n")
        aws_resource = input("Digite o recurso que você quer restringir: ")
        print("\n")

        dict_variables["policies"].update({str(nome_policia) : {  "action" : str(aws_action), \
                                                                "resource" : str(aws_resource)}})

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

    criar_politicas = input("Você gostaria de criar restrições a esse usuário? (y/n)")

    while confere_resposta_nao_valida(criar_politicas):
        criar_politicas = input("Você gostaria de criar restrições a esse usuário? (y/n)")

    if criar_politicas == "y" or criar_politicas == "Y":
        criar_restricoes()
    elif criar_politicas == "n" or criar_politicas == "N":
        print("Ok, vamos continuar então" + "\n")


def info_basicas():
    print("Agora vamos para detalhes da AWS" + "\n")
    region = input("Digite a região do projeto: ")
    print("\n")

    dict_variables.update({str("aws_region") : str(region)})
    escreve_documento(dict_variables)


def cria_sec_group():
    print("""Vamos criar um grupo de segurança para a instância" \n""")

    security_group_name = input("""Digite o nome do grupo de segurança: 
    R: """)
    print("\n")

    dict_variables.update({"sec_group" : security_group_name})


    print("Agora vamos para as regras do grupo de segurança. Mas antes..." + "\n")

    criar_regras = input("Você gostaria de criar regras para o grupo de segurança? (y/n)")  

    if criar_regras == "y" or "Y":

        qtd_regras = input("Quantas regras você quer criar?")

        for i in range(int(qtd_regras)):
            nome_regra = input("Digite o nome da regra: ")
            print("\n")
            description_security_group = input("Digite a descrição do grupo de segurança: ")
            print("\n")
            aws_from_port = input("Digite a porta de origem: ")
            print("\n")
            aws_to_port = input("Digite a porta de destino: ")
            print("\n")
            aws_protocol = input("Digite o protocolo: ")
            print("\n")
            aws_cidr_blocks = input("Digite o bloco de ip: ")

            dict_variables["sg_ingress_rules"].update({str(nome_regra) : {  "description" : str(description_security_group), \
                                                                            "from_port" : str(aws_from_port), "to_port" : str(aws_to_port), \
                                                                            "protocol" : str(aws_protocol), "cidr_blocks" : [str(aws_cidr_blocks)]}})
    
    escreve_documento(dict_variables)





def create_variables():

    qtd_instancias = input("\n Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar?" + "\n")

    while confere_se_eh_numero(qtd_instancias):
        qtd_instancias = input("\n Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar?" + "\n")

    for contador in range(int(qtd_instancias)):
        name_instance = input("""Digite o nome da instância: 
        
        R: """)
        nome_instancias.append(name_instance)

        image_id = input("""Digite o id da imagem a ser utilizada no servidor: 
        
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

        print("\n")

        sec_group = input("Você quer criar um security group com regras? (y/n)")

        while confere_resposta_nao_valida(sec_group):
            sec_group = input("Você quer criar um security group com regras? (y/n)")

        if sec_group == "y" or sec_group == "Y":
            cria_sec_group()
        elif sec_group == "n" or sec_group == "N":
            print("Ok, então o grupo de segurança vai ser padrão" + "\n")

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
    destruir = input("""Qual recurso você gostaria de destruir:
    1- Instância;
    2- Grupo de sergurança;
    3- Usuário
    
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
            escreve_documento(dict_variables)
        elif destruir_yes_no == "n" or "N":
            print("Ok, então não destruiremos a instância" + "\n")

    elif destruir == "2":
        sec_group_destruir = input(""" Você escolheu destruir um grupo de segurança.
        Digite o nome do grupo de segurança que você quer destruir: 
        R: """)

        regras = dict_variables["sg_ingress_rules"]

        destruir_yes_no = input("""Você está prestes a destruir o grupo de segurança {sec_group_destruir}, que possui as seguintes regras:
        {regras} "\n" 
        
        Você tem certeza que quer destruir o grupo de segurança? (y/n)
        R: """)

        while confere_resposta_nao_valida(destruir_yes_no):
            destruir_yes_no = input("Você tem certeza que quer destruir o grupo de segurança? (y/n)")

        if destruir_yes_no == "y" or "Y":
            print("Ok, destruindo o grupo de segurança" + "\n")
            dict_variables.pop("sec_group")
            dict_variables.pop("sg_ingress_rules")
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


def listar_recursos():
    print("Mas antes vamos garantir que o programa está atualizado... Aguarde um momento")

    os.system("terraform refresh")

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
        os.system("terraform output sg_ingress_rules")
    elif escolha_listar == "3":
        print("Você escolheu listar usuários" )
        os.system("terraform output aws_iam_users")

def main():

    print("Olá caro usuário, seja bem vindo ao nosso projeto de automação de infraestrutura" + "\n")


    primeira_resposta = input("""Primeiramente, você gostaria de :
    
    1- Iniciar uma instância existente;
    2- Parar uma instância existente;
    3- Criar uma nova instância;
    4- Destruir algum recurso;
    5 - Listar recursos;
    6 - Criar um usuário 
    
    R: """)

    # info_basicas()


    if primeira_resposta == "1":
        print("Você escolheu iniciar uma instância existente" + "\n")
        region = input("Digite a região da instância que você quer iniciar: ")
        lambda_handler_inicia(None, None, region)
    elif primeira_resposta == "2":
        print("Você escolheu parar uma instância existente" + "\n")
        region = input("Digite a região da instância que você quer parar: ")
        lambda_handler_para(None, None, region)
    elif primeira_resposta == "3":
        print("Você escolheu criar uma nova instância" + "\n")

        # Cria o arquivo variables.tfvars
        create_variables()

        # os.system("terraform init")
        # os.system("source ~/.bashrc")
        # os.system("terraform plan")
        # os.system("terraform apply")

    elif primeira_resposta == "4":
        print("Você escolheu destruir algum recurso" + "\n")
        destruir_recurso()
    elif primeira_resposta == "5":
        print("Você escolheu listar recursos" + "\n")
        listar_recursos
    elif primeira_resposta == "6":
        print("Você escolheu criar um usuário" + "\n")
        criar_usuario()




# Executa a função main
main()





# os.system("terraform output password | base64 -d > test.txt")

# os.system("gpg --decrypt test.txt > file.txt")

# region_global = "us-east-1"

# lambda_handler_para(None, None, region = region_global)

# lambda_handler(None, None, region = region_global)
