# AWS-projeto-Cloud <img src="https://img.shields.io/static/v1?label=B&message=Finalizado&color=success&style=flat-square&logo=ghost"/>

## Feito por :raising_hand_woman:

- Lívia Sayuri Makuta.


## Linguagem, ferramenta e plataforma utilizadas:

- <img src="https://img.shields.io/static/v1?label=Code&message=Python&color=blue&style=plastic&labelColor=black&logo=python"/>

- <img src="https://img.shields.io/static/v1?label=Code&message=Terraform&color=purple&style=plastic&labelColor=black&logo=Terraform"/>

- <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>

## Objetivo do projeto :round_pushpin: :

O objetivo do projeto é facilitar e automatizar a criação de uma infraestrutura em nuvem utilizando como provedora a AWS (Amazon Web Services). E, para fazer
essa automatização funcionar a ferramenta do Terraform foi integrada com Python. Dessa forma, é no Python que o usuário irá escolher suas preferências em relação à região da AWS em que irá mexer, quais instâncias irá criar, seus security groups, entre outros, enquanto o Terraform é responsável por subir tudo aquilo que o usuário estiver demandando.


## O que é o Terraform? :thinking:

Antes é importante que alguns tópicos sejam esclarecidos:
- O Terraform é uma ferramenta open source que permite criar e alterar partes da infraestrutura em nuvem através de blocos de código, o que abrange o conceito de infraestrutura como código (IaC : "Infrastructure as code"). 
- Além disso, possui uma linguagem declarativa, ou seja, o usuário descreve exatamente como ele quer os recursos, como por exemplo uma máquina, mas não sabe exatamente como essa máquina será provisionada. 
- Cada vez que é executado, o Terraform gera planos de execução que descrevem o que será feito para atingir aquilo que foi pedido pelo projetista da arquitetura, o que é extremamente útil para ter ambientes que possam ser reproduzidos depois.

## Pré-requisitos :heavy_check_mark:

Antes de começar a entender como o projeto foi desenvolvido, primeiro é necessário que algumas isntalações e configurações sejam feitas. A começar pela instação do Terraform. Como todo o projeto foi desenvolvido no ambiente do **Ubuntu 20.04 LTS**, os comandos que serão citados ao decorrer desse tutorial são mais voltados a este sistema operacional. 

Assim, para **instalar o terraform**, crie uma pasta que será a pasta usada para o projeto, abra o terminal e rode os seguintes comandos:

`sudo apt-get update && sudo apt-get install -y gnupg software-properties-common`

`wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg`

`gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint`

`echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

`sudo apt update`

`sudo apt-get install terraform`

Para mais detalhes sobre o que faz cada comando, consultar o site do terraform da qual o tutorial foi retirado: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli. 

Além disso, também é recomendado **baixar a interface de linhas de comando (CLI) da AWS**. Para isso, basta seguir o tutorial disponível em: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html . 

Por fim, não menos importante, você precisa ter credenciais na AWS: o ACESS_KEY_ID e o SECRET_ACCESS_KEY. É por meio dessas credenciais que você conseguirá utilizar os recursos da AWS no Terraform. Sendo assim, mais uma vez abra o terminal e (no caso do sistema operacional Linux) procure pelo documento .bashrc (normalmente ele fica na root ~). 

Abra o documento:

`nano .bashrc`

E escreva no fim do documento as seguintes linhas:

export AWS_ACCESS_KEY_ID= <SUA_ACCESS_KEY>

export AWS_SECRET_ACCESS_KEY= <SUA_SECRET_ACCESS_KEY>

Feito isso, volte para a pasta onde está trabalhando e rode o seguinte comando:

`source ~/.bashrc`

**Cuidado**: não publique essas chaves de maneira alguma.


## Iniciando :computer:


Depois de instalar e de configurar tudo o que era necessário, agora sim você pode clonar este repositório. Para isso basta abrir o terminal na pasta que você criou e digitar o seguinte comando:

`git clone https://github.com/Lihsayuri/AWS-projeto-Cloud`

Entre na pasta learn-terraform-aws-instance e abra o documento main_project.py em seu editor de código favorito (aconselho abrir no VsCode). 

Depois é só rodar o código e ir respondendo as questões perguntadas no próprio terminal. 

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

De maneira geral o código foi construído por meio de uma função principal : a main, que chama várias outras funções de acordo com as respostas do usuário. Ou seja, essa aplicação tem um loop principal que é responsável por sempre carregar o menu até que o usuário peça para sair (ou caso aconteça algum erro que infelizmente não tenha sido tratado, mas nesse caso basta rodar a aplicação e tentar de novo). A partir desse loop, outras funções vão sendo chamadas e vão escrevendo todas as respostas do usuário em um arquivo de variáveis no formato json (por ser mais fácil de manipular em conjunto com o Python).

E são essas variáveis que serão preenchidas nos blocos de código dos arquivos do Terraform. Dessa forma, a estrutura e a conexão do Python com o Terraform pode ser descrita de seguinte forma:

- O Python retém as informações do usuário e as utiliza para escrever um arquivo de variáveis no formato json.
- Esse arquivo no formato json é interpretado pelo Terraform como os valores de entrada para as variáveis que possuem seu formato descrito e que foram declaradas no arquivo `variables.tf`. 
- Cada variável do arquivo `variables.tf` pode ser chamada por outros arquivos do terraform (que são blocos de código criando recursos e captando informções importantes) através de uma citação var.(nome da variável).
- Logo, a sequência é: informação sai do Python e vai pro arquivo json, esse arquivo json provê os valores de entrada para as variáveis declaradas em `variables.tf`, e essas variáveis vão sendo preenchidas nos arquivos do Terraform sendo usadas de uma maneira dinâmica - isto é, que pode mudar, não será sempre a mesma coisa [a não ser que o usuário sempre peça as mesmas coisas].

Vale lembrar que no programa em Python foram feitas algumas conferências em relação à resposta do usuário, como checagens para algumas respostas mas não para todas. Dessa forma, certifique-se de responder exatamente aquilo que está sendo pedido.

Ademais, é importante ressaltar que como o objetivo é automatizar e facilitar o uso da AWS através do Terraform, muitos dos recursos são de certe forma pré-definidos. Por exemplo, caso o usuário quando for criar outros usuários queira estabelecer certas restrições para esses, ele poderá escolher entre três opções de restrição: apenas ler, apenas ler e criar, e apenas ler, criar e deletar.


## Vídeo com exemplo de funcionamento :movie_camera: :camera:

[a ser gravado]

## Notas finais :bookmark:

Faça bom uso da aplicação e caso utilize algo retirado daqui, faça referências ao repositório.
Quaisquer dúvidas sobre o código ou a aplicação, entrar em contato com @Lihsayuri.

## Referências:

- Terraform (documentação e exemplos de códigos)

