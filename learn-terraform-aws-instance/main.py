import click
import os
import boto3
import json

contador = 0
dict_variables = {"virtual_machines" : {}}

# Função que cria o arquivo variables.tfvars



@click.command()
@click.option('--name', prompt='Bem vindo a aplicação do Terraform! Escolha dentre as seguintes opções', type = click.Choice([1, 2, 3, 4, 5], case_sensitive=False)
              help='A opção que você quer escolher.')



def hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")

if __name__ == '__main__':
    hello()












# def create_variables():
#     # Cria o arquivo variables.tfvars

#     print("Então, pronto para começar a construir a infraestrutura? Vamos começar com o seu usuário a ser criado" + "\n")
#     username = input("Digite o seu nome de usuário: ")
#     print("\n")

#     dict_variables.update({str("aws_user_name") : str(username)})
#     json_object_user = json.dumps(dict_variables, indent = 4)
#     with open('.auto.tfvars.json', 'w') as outfile:
#         outfile.write(json_object_user)

#     print("Agora vamos para detalhes da AWS" + "\n")
#     region = input("Digite a região do projeto: ")
#     print("\n")

#     dict_variables.update({str("aws_region") : str(region)})
#     json_object_region = json.dumps(dict_variables, indent = 4)
#     with open('.auto.tfvars.json', 'w') as outfile:
#         outfile.write(json_object_region)

#     qtd_instancias = input("\n Agora vamos para informações sobre a instância que você quer criar. Primeiro, quantas instâncias você quer criar?" + "\n")

#     for contador in range(int(qtd_instancias)):
#         name_instance = input("Digite o nome da instância: ")

#         image_id = input("\n  Digite o id da imagem a ser utilizada no servidor: ")
#         print("\n")
#         print("Agora você tem que escolher o tipo da instância a ser usada no servidor" + "\n")
#         instance_type_choice = input("\n  Você pode escolher dentre as seguintes: [1 - t2.micro, 2 - t2.small, 3 - t2.medium, 4- t2.large]?")
#         if instance_type_choice == "1":
#             instance_type = "t2.micro"
#         elif instance_type_choice == "2":
#             instance_type = "t2.small"
#         elif instance_type_choice == "3":
#             instance_type = "t2.medium"
#         elif instance_type_choice == "4":
#             instance_type = "t2.large"
#         else:
#             print("Você não escolheu uma opção válida, então a instância será do tipo t2.micro" + "\n")
#             instance_type = "t2.micro"
#         dict_variables["virtual_machines"].update({str(name_instance) : {"image_id" : str(image_id), "instance_type" : str(instance_type)}})
#         json_object = json.dumps(dict_variables, indent = 4)
#         with open('.auto.tfvars.json', 'w') as outfile:
#             outfile.write(json_object)

#         print("\n")


#     sec_group = input("Você quer criar um security group? (y/n)")

#     if sec_group == "y":
#         print("Vamos criar um grupo de segurança para a instância" + "\n")
#         security_group_name = input("Digite o nome do grupo de segurança: ")
#         print("\n")
#         description_security_group = input("Digite a descrição do grupo de segurança: ")
#         print("\n")
#         aws_from_port = input("Digite a porta de origem: ")
#         print("\n")
#         aws_to_port = input("Digite a porta de destino: ")
#         print("\n")
#         aws_protocol = input("Digite o protocolo: ")
#         print("\n")
#         aws_cidr_blocks = input("Digite o bloco de ip: ")
#     elif sec_group == "n":
#         # dict_variables["virtual_machines"].update({"name" : "", "instance_type" : str(instance_type)})
#         print("Ok, então não criaremos um grupo de segurança" + "\n")

# def lambda_handler_para(event, context, region):
#     instances = [input("Agora digite o id da instância que você quer parar: ")]
#     ec2 = boto3.client('ec2', region_name=region)
#     ec2.stop_instances(InstanceIds=instances)
#     print('stopped your instances: ' + str(instances))


# def lambda_handler_inicia(event, context, region):
#     instances = [input("Agora digite o id da instância que você quer começar: ")]
#     ec2 = boto3.client('ec2', region_name=region)
#     ec2.start_instances(InstanceIds=instances)
#     print('started your instances: ' + str(instances))

# def main():

#     print("Olá caro usuário, seja bem vindo ao nosso projeto de automação de infraestrutura" + "\n")

#     primeira_resposta = input("Primeiramente, você gostaria de : 1- iniciar uma instância existente, 2- parar uma instância existente, 3- criar uma nova instância?, 4- destruir algum recurso, \
#         ou 5 - listar recursos?" + "\n")

#     if primeira_resposta == "1":
#         print("Você escolheu iniciar uma instância existente" + "\n")
#         region = input("Digite a região da instância que você quer iniciar: ")
#         lambda_handler_inicia(None, None, region)
#     elif primeira_resposta == "2":
#         print("Você escolheu parar uma instância existente" + "\n")
#         region = input("Digite a região da instância que você quer parar: ")
#         lambda_handler_para(None, None, region)
#     elif primeira_resposta == "3":
#         print("Você escolheu criar uma nova instância" + "\n")

#         # Cria o arquivo variables.tfvars
#         create_variables()

#         os.system("terraform init")

#         os.system("source ~/.bashrc")

#         # os.system("terraform output password | base64 -d > test.txt")

#         # os.system("gpg --decrypt test.txt > file.txt")

#         os.system("terraform plan")

#         os.system("terraform apply")
#     elif primeira_resposta == "4":
#         print("Você escolheu destruir algum recurso" + "\n")
#         destruir = input("Qual recurso você gostaria de destruir 1- instância, 2- grupo de sergurança, ou 3- usuário? ")
#         if destruir == "1":
#             print("Você escolheu destruir uma instância" + "\n")
#             os.system("terraform destroy --target aws_instance.app_server")
#         elif destruir == "2":
#             print("Você escolheu destruir um grupo de segurança" + "\n")
#             os.system("terraform destroy --target aws_security_group.allow_tls")
#         elif destruir == "3":
#             print("Você escolheu destruir um usuário" + "\n")
#             os.system("terraform destroy --target aws_iam_user.user")
#         else:
#             print("Você não escolheu uma opção válida" + "\n")
#     elif primeira_resposta == "5":
#         print("Você escolheu listar recursos" + "\n")
#         os.system("terraform show")


# # Executa a função main
# main()





