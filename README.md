# AWS-projeto-Cloud <img src="https://img.shields.io/static/v1?label=A&message=Finalizado&color=success&style=flat-square&logo=ghost"/>

## Feito por :raising_hand_woman:

- Lívia Sayuri Makuta.


## Linguagem, ferramenta e plataforma utilizadas:

- <img src="https://img.shields.io/static/v1?label=Code&message=Python&color=blue&style=plastic&labelColor=black&logo=python"/>

- <img src="https://img.shields.io/static/v1?label=Code&message=Terraform&color=purple&style=plastic&labelColor=black&logo=Terraform"/>

- <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>


## Conceito C

- Implementar criação automática de VPC e sub-rede :heavy_check_mark:
- Listar instâncias e regiões, usuários e security_groups com regras :heavy_check_mark:
- Parar e iniciar instâncias :heavy_check_mark:
- Criação de instâncias e pelo menos 2 tipos de hosts :heavy_check_mark:
- Criação de security groups padrões e associação a instâncias :heavy_check_mark:
- Criação de usuário no IAM :heavy_check_mark:
- Deletar usuários, instâncias e security groups :heavy_check_mark:

## Conceito B

- Regras personalizadas em security groups :heavy_check_mark:
- Instâncias em mais de uma região (us-east-1 e us-west-1) :heavy_check_mark:
- Associar restrições a usuários (apenas consultar, apenas consultar e criar e apenas consultar, criar e deletar) :heavy_check_mark:
- Deletar regras em security groups :heavy_check_mark:


## Conceito A

- Criar um HA de servidores web :heavy_check_mark: 


## Objetivo do projeto :round_pushpin: :

O objetivo do projeto é facilitar e automatizar a criação de uma infraestrutura em nuvem utilizando como provedora a AWS (Amazon Web Services). E, para fazer
essa automatização funcionar, a ferramenta do Terraform foi integrada com Python. Dessa forma, é no Python que o usuário irá escolher suas preferências em relação à região da AWS em que irá mexer, quais instâncias irá criar, seus security groups, entre outros, enquanto o Terraform é responsável por subir tudo aquilo que o usuário estiver demandando.


## O que é o Terraform? :thinking:

Antes é importante que alguns tópicos sejam esclarecidos:
- O Terraform é uma ferramenta open source que permite criar e alterar partes da infraestrutura em nuvem através de blocos de código, o que abrange o conceito de infraestrutura como código (IaC : "Infrastructure as code"). 
- Além disso, possui uma linguagem declarativa, ou seja, o usuário descreve exatamente como ele quer os recursos, como por exemplo uma máquina, mas não sabe exatamente como essa máquina será provisionada. 
- Cada vez que é executado, o Terraform gera planos de execução que descrevem o que será feito para atingir aquilo que foi pedido pelo projetista da arquitetura, o que é extremamente útil para ter ambientes que possam ser reproduzidos depois.

## Pré-requisitos :heavy_check_mark:

Antes de começar a entender como o projeto foi desenvolvido, primeiro é necessário que algumas instalações e configurações sejam feitas. A começar pela instação do Terraform. Como todo o projeto foi desenvolvido no ambiente do **Ubuntu 20.04 LTS**, os comandos que serão citados ao decorrer desse tutorial são mais voltados a este sistema operacional. 

### Instalação do Terraform

Assim, para **instalar o terraform**, crie uma pasta que será a pasta usada para o projeto, abra o terminal e rode os seguintes comandos:

`sudo apt-get update && sudo apt-get install -y gnupg software-properties-common`

`wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg`

`gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint`

`echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

`sudo apt update`

`sudo apt-get install terraform`

Para mais detalhes sobre o que faz cada comando, consultar o site do terraform da qual o tutorial foi retirado: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli. 

### Instalação do CLI da AWS e do boto3 

Além disso, também é recomendado **baixar a interface de linhas de comando (CLI) da AWS**. Para isso, basta seguir o tutorial disponível em: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html . E, como também foi utilizado no projeto para consultar informações do dashboard da AWS, é necessário baixar a biblioteca boto3. Para isso, basta rodar o comando abaixo:

`pip install boto3`

### Configuração de credenciais

Por fim, não menos importante, você precisa ter credenciais na AWS: o ACESS_KEY_ID e o SECRET_ACCESS_KEY. É por meio dessas credenciais que você conseguirá utilizar os recursos da AWS no Terraform. Sendo assim, mais uma vez abra o terminal e (no caso do sistema operacional Linux) procure pelo documento .bashrc (normalmente ele fica na root ~). 

Abra o documento:

`nano .bashrc`

E escreva no fim do documento as seguintes linhas:

```
export AWS_ACCESS_KEY_ID= <SUA_ACCESS_KEY>

export AWS_SECRET_ACCESS_KEY= <SUA_SECRET_ACCESS_KEY>

```

Feito isso, volte para a pasta onde está trabalhando e rode o seguinte comando:

`source ~/.bashrc`

Ainda você também terá que colocar essas chaves em outro documento. Mais uma vez vá até o diretório raiz e procure pela pasta `.aws`. Acesse-a pelo terminal e crie um documento chamado credentials, através do comando abaixo:

`touch credentials`

Depois edite o documento através do comando:

`nano credentials`

Escreve as seguintes linhas:

```[default]
aws_access_key_id=<sua_access_key>
aws_secret_access_key=<sua_secret_access_key>
```

#### CUIDADO :warning: :no_entry_sign: : NÃO PUBLIQUE ESSAS CHAVES DE MANEIRA ALGUMA.


### Conferir permissões

Com tudo isso feito, confira que seu usuário possui todas as permissões de administrador, é isso que irá possibilitar você criar, listar e deletar recursos em diferentes regiões. Para isso, comece acessando o console:


![WhatsApp Image 2022-11-24 at 21 33 51](https://user-images.githubusercontent.com/62647438/203878313-dad61a6c-53d3-435f-93c4-2c3bdfe6cb81.jpeg)


Feito isso, acesse a aba do IAM e encontre o seu usuário. Feito isso, clique nele e confira se você possui a permissão de administrador, como pode ser visto abaixo:


![WhatsApp Image 2022-11-24 at 21 33 35](https://user-images.githubusercontent.com/62647438/203878325-547cab91-aa01-4bd3-b9d2-83ffd090226d.jpeg)


Pronto, agora sim vamos à aplicação.



## Iniciando sobre a aplicação :computer:


Depois de instalar e de configurar tudo o que era necessário, agora sim você pode clonar este repositório. Para isso basta abrir o terminal na pasta que você criou e digitar o seguinte comando:

`git clone https://github.com/Lihsayuri/AWS-projeto-Cloud`

Entre na pasta learn-terraform-aws-instance e abra o documento main_project.py em seu editor de código favorito (aconselho abrir no VsCode). 

Depois é só rodar o código e ir respondendo as questões perguntadas no próprio terminal. A seguinte tela deverá ser vista por você:

![WhatsApp Image 2022-11-24 at 21 36 40](https://user-images.githubusercontent.com/62647438/203878531-235f3c0e-8a71-4a97-aa30-ba5ccb7db613.jpeg)


Você poderá escolher entre as seguintes opções no menu:

        
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


Basta escolher uma dessas opções que o programa fará o resto para você. É recomendado ler o manual antes de escolher as outras opções.


## Manual de uso :bookmark_tabs: :

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
    - Para acessar a senha do usuário e poder mexer no console da AWS, primeiro você terá que selecionar a opção para aplicar as mudanças e depois de aplicadas, como output do programa você terá as informações sobre os usuários criados, o que inclue as senhas de 10 dígitos.


## Informações sobre a construção do código  :construction_worker: :computer:

De maneira geral o código da aplicação foi construído no arquivo `main_project.py` por meio de uma função principal : a `main()`, que chama várias outras funções de acordo com as respostas do usuário. Ou seja, essa aplicação tem um loop principal que é responsável por sempre carregar o menu até que o usuário peça para sair (ou caso aconteça algum erro que infelizmente não tenha sido tratado, mas nesse caso basta rodar a aplicação e tentar de novo :) ). A partir desse loop, outras funções vão sendo chamadas e vão escrevendo todas as respostas do usuário em um arquivo de variáveis no formato json (por ser mais fácil de manipular em conjunto com o Python).

E são essas variáveis que serão preenchidas nos blocos de código dos arquivos do Terraform. Dessa forma, a estrutura e a conexão do Python com o Terraform pode ser descrita de seguinte forma:

- O Python retém as informações do usuário e as utiliza para escrever um arquivo de variáveis no formato json.
- Esse arquivo no formato json é interpretado pelo Terraform como os valores de entrada para as variáveis que possuem seu formato descrito e que foram declaradas no arquivo `variables.tf`. 
- Cada variável do arquivo `variables.tf` pode ser chamada por outros arquivos do terraform (que são blocos de código criando recursos e captando informações importantes) através de uma citação var.(nome da variável).
- Logo, a sequência é: informação sai do Python e vai pro arquivo json, esse arquivo json provê os valores de entrada para as variáveis declaradas em `variables.tf`, e essas variáveis vão sendo preenchidas nos arquivos do Terraform sendo usadas de uma maneira dinâmica - isto é, que pode mudar, não será sempre a mesma coisa [a não ser que o usuário sempre peça as mesmas coisas].

Vale lembrar que no programa em Python foram feitas algumas conferências em relação à resposta do usuário, como checagens para algumas respostas mas não para todas. Dessa forma, **certifique-se de responder exatamente aquilo que está sendo pedido**.

Ademais, é importante ressaltar que como o objetivo é automatizar e facilitar o uso da AWS através do Terraform, muitos dos recursos são de certe forma pré-definidos. Por exemplo, caso o usuário quando for criar outros usuários queira estabelecer certas restrições para esses, ele poderá escolher entre três opções de restrição: apenas ler, apenas ler e criar, e apenas ler, criar e deletar.


## Detalhamento sobre a construção do código 

## Arquivos principais do Terraform

A essa altura você já deve ter entendido que o Terraform é quem provisionará todos os recursos necessários para construir a infraestrutura. Mas como? Bem, como dito antes, o Terraform possui uma linguagem declarativae cada bloco de código possui uma função. Dentre eles temos os: resources, data e outputs. Os `resources` são responsáveis por descrever os recursos a serem criados, enquanto o `data` representa dados que podem ser usados pelo Terraform embora possam ter sido definidos fora dele, e os `outputs` são dados retornados pelo próprio Terraform que informam sobre a sua infraestrutura.

E como esses blocos foram organizados? Para cada região - no caso do projeto estamos usando apenas a `us-east-1` e a `us-west-1` - cada infraestrutura é formada pelos seguintes arquivos Terraform: `main.tf`, `instances.tf`, `sec_group`, `autoscaling.tf`, `data.tf` e `output.tf`. E são estruturados da seguinte maneira:

- main.tf: É no main que os recursos básicos como nosso provedor, região, VPC, subnetes e gateway são provisionados. É a partir dessa estrutura básica que será possível criar instâncias e security groups e suas regras. Lembre-se: a sua nuvem virtual privada está dentro de uma região e possui subnetes onde as instâncias serão criadas. 

- instances.tf : É nesse documento que as instâncias são criadas e que security groups são associados. 

- sec_group.tf: É nesse documento que os security groups e suas regras são criados. 

- autoscaling.tf: É nesse documento que o Load Balancer, o Auto-Scaling Group e a configuração para começar uma nova instâncias estão configurados. 

Como exemplo, temos um pedaço do código do `main.tf` abaixo:

``` terraform 
resource "aws_vpc" "main" {
  cidr_block       =    var.vpc_cidr_block 
  instance_tenancy = "default"

  tags = {
    name = "VPC_certa${var.aws_region}"
  }
}
```

Lembra que eu havia comentado sobre o `var.[nome_da_variável]`? Pois é, você vai enteder a importâncias desse argumento


## Variáveis no projeto

É por isso que o arquivo `variables.tf` existe. Nele foram declaradas todas as variáveis que seriam usadas de maneira dinâmica, isto é, aquelas que não são sempre fixas e que o usuário tem o poder de escolha. Mas esse documento apenas declara o formato das variáveis como você pode ver abaixo:

``` terraform
variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "A região da AWS para fazer o deploy do servidor."
}

variable "vpc_cidr_block" {
  type        = string
  default     =  "10.0.0.0/16"
}

variable "virtual_machines" {
  description = "Informações sobre cada máquina a ser criada"
  type = map(object({
    image_id = string
    instance_type = string
  }))
}

```

As variáveis preenchidas mesmo vem de um outro arquivo : o .auto.tfvars.json (que muda um pouquinho de nome dependendo da região). É nele que os inputs do usário serão inseridos, e é daí que as variáveis declaradas no `variables.tf` irão buscar as informações. E, com elas corretamente definidas, basta apenas chamar o argumento `var.` mais o nome da variável de interesse que esses valores dinamicamente configurados serão preenchidos pelos blocos de `resources` nos outros arquivos do Terraform. 

Para você visualizar melhor esse arquivo em `.json`, um exemplo dele pode ser visto abaixo:


``` json
{
    "aws_region": "us-east-1",
    "vpc_cidr_block": "10.0.0.0/16",
    "virtual_machines": {
        "vm1": {
            "image_id": "ami-0149b2da6ceec4bb0",
            "instance_type": "t2.micro"
        },
        "vm2": {
            "image_id": "ami-0149b2da6ceec4bb0",
            "instance_type": "t2.micro"
        }
    }
}
```

Mas e se eu quiser criar vários recursos de uma vez? É aqui que entra a função `for_each`, que é capaz de percorrer listas, maps e objetos para definir uma variável com múltiplos valores - que é o que permite criar múltiplas instâncias, security groups e usuários. Um exemplo dela em ação pode ser visto a seguir:

``` terraform
resource "aws_instance" "app_server" {
  for_each = var.virtual_machines
  ami           =  each.value.image_id 
  instance_type =  each.value.instance_type  
  key_name = "livia_certo"
  subnet_id = aws_subnet.public.id
  vpc_security_group_ids = [for sec_name in var.sec_group_instances[each.key].sec_names : aws_security_group.allow[sec_name].id]

  tags = {
    Name = "IdGroup-${each.key}"
  }

}
```

## Regiões, VPCs e Subnets

Como comentado anteriormente estamos trabalhando apenas com 2 regiões, e isso foi feito através do Python que troca de pastas dependendo da região que o usuário escolher - a us-east-1 ou a us-west-1. Sendo assim, tudo aquilo que o usuário der deploy em uma região, ficará naquela região - do mesmo modo, tudo o que ele destruir naquela região será destruído apenas ali. 

Além disso, dentro de cada região existe uma VPC com valores de IP fixos e sem possibilidade de ser alterado pelo usuário: no caso da região us-east-1 o bloco CIDR é 10.0.0.0/16 e no caso da região us-west-1 este bloco muda para: 172.16.0.0/16. Por fim, as subnets ficam dentro de cada uma dessas VPCs e também são determinadas levando em consideração o próprio intervalo de IPs da VPC.

### Usuários

Para criar os usuários, foi criada uma pasta separada com recursos e dados apenas para esse fim, isso porque independente da região acessada, os usários são os mesmos. Dessa forma, da maneira que o projeto foi feito, os recursos dos usuários estão contemplados no documento `iam.tf` e seus dados e outputs em `data.tf` e `output.tf`, respectivamente (todos esses documentos estão dentro da pasta terraform-users).

Toda vez que você criar um usuário e aplicar as mudanças, como output você verá a senha informações e a senha de acesso ao console da AWS desse usuário criado. 

### High Availability

Por fim, foi implementada alta disponibilidade para servidores web na região us-east-1. Dessa forma, quando uma instância com a imagem criada por mim for lançada, se o seu consumo de CPU chegar a 50% em média, em cerca de 2 minutos uma nova instância será criada. E caso isso ocorra novamente, mais outra instância será lançada - isso porque configurei no máximo 3 instâncias para suprir a necessidade na aplicação. Além disso, se depois de 2 minutos a média de consumo for menor que 10%, essas instâncias serão desligadas. Isso pode ser testado com um teste de stress que pode ser feito com o seguinte comando após ter acessada a instância via ssh:

`stress --cpu 8 --timeout 300`

Isso é possível pois o load balancer aponta para um grupo - o target group- que foi definido com as instâncias. Dessa forma, através de alarmes que estarão monitorando o uso da CPU, conforme o limite seja atingido (tanto acima quanto abaixo), ele executará uma `policy` configurada que irá criar ou desligar as instâncias. E quando ela for criada, ela utilizará como imagem um template criado por mim que já possui uma simples aplicação web-server só para testes, além de já possuir o módulo `stress` instalado. Lembrando que para cada recurso as portas certas foram liberadas para permitir o acesso à aplicação e ao ssh. 

**Atenção: o teste demora um pouco, mais está funcionando :) e isso foi implementado apenas para a região us-east-1** 


## Notas finais :bookmark:

Faça bom uso da aplicação e caso utilize algo retirado daqui, faça referências ao repositório.
Quaisquer dúvidas sobre o código ou a aplicação, entrar em contato com @Lihsayuri.

## Referências:

- Terraform (documentação e exemplos de códigos);
- Roteiros de aula e os professores: Rodolfo Avelino e Tiago Demay.

