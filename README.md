# AWS-projeto-Cloud <img src="https://img.shields.io/static/v1?label=A&message=Finalizado&color=success&style=flat-square&logo=ghost"/>

## Created by :raising_hand_woman:

- Lívia Sayuri Makuta.


## Languages, Tools, and Platforms Used:

- <img src="https://img.shields.io/static/v1?label=Code&message=Python&color=blue&style=plastic&labelColor=black&logo=python"/>

- <img src="https://img.shields.io/static/v1?label=Code&message=Terraform&color=purple&style=plastic&labelColor=black&logo=Terraform"/>

- <img src="https://img.shields.io/badge/Amazon_AWS-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white"/>


## Concept C

- Implement automatic creation of VPC and subnets :heavy_check_mark:
- List instances and regions, users, and security groups with rules :heavy_check_mark:
- Stop and start instances :heavy_check_mark:
- Create instances with at least 2 types of hosts :heavy_check_mark:
- Create default security groups and associate them with instances :heavy_check_mark:
- Create users in IAM :heavy_check_mark:
- Delete users, instances, and security groups :heavy_check_mark:

## Concept B

- Custom rules in security groups :heavy_check_mark:
- Instances in multiple regions (us-east-1 and us-west-1) :heavy_check_mark:
- Associate restrictions to users (read-only, read/create, and read/create/delete) :heavy_check_mark:
- Delete rules in security groups :heavy_check_mark:


## Concept A

- Create a highly available web server setup :heavy_check_mark: 


## Project Objective :round_pushpin: :

The objective of this project is to facilitate and automate the creation of cloud infrastructure using AWS (Amazon Web Services) as the provider. To make this automation work, the Terraform tool was integrated with Python. This way, the user can choose their preferences regarding the AWS region, which instances to create, security groups, among others, while Terraform is responsible for provisioning everything the user demands.


## What is Terraform? :thinking:

It’s important to clarify a few points:

- Terraform is an open-source tool that allows you to create and modify parts of cloud infrastructure through code blocks, encompassing the concept of Infrastructure as Code (IaC).
- Additionally, it has a declarative language, meaning the user describes exactly how they want the resources (e.g., a machine) without needing to know how that machine will be provisioned.
- Every time it runs, Terraform generates execution plans that describe what will be done to achieve what the architect of the infrastructure requested, which is extremely useful for creating reproducible environments later.

## Prerequisites :heavy_check_mark:

Before starting to understand how the project was developed, certain installations and configurations need to be made. First, install Terraform. Since the entire project was developed on **Ubuntu 20.04 LTS**, the commands mentioned throughout this tutorial are geared towards this operating system.

### Installing Terraform

To **install Terraform**, create a directory for the project, open the terminal, and run the following commands:

`sudo apt-get update && sudo apt-get install -y gnupg software-properties-common`

`wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg`

`gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint`

`echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list`

`sudo apt update`

`sudo apt-get install terraform`

For more details on what each command does, consult the Terraform installation tutorial: https://developer.hashicorp.com/terraform/tutorials/aws-get-started/install-cli. 

### Installing AWS CLI and Boto3

Additionally, it is recommended to **download the AWS Command Line Interface (CLI)**.  For that, simply follow the tutorial available at: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html . Since Boto3 was also used in the project to query information from the AWS dashboard, you need to install it as well. Run the command below:

`pip install boto3`

### Configuring Credentials

Finally, it is crucial to have AWS credentials: o ACESS_KEY_ID e o SECRET_ACCESS_KEY. É por meio dessas credenciais que você conseguirá utilizar os recursos da AWS no Terraform. These credentials allow you to use AWS resources in Terraform. Open the terminal and locate the .bashrc document (usually found in the root ~ directory) on your Linux system.

Open the document:

`nano .bashrc`

Then, add the following lines at the end of the document:

```
export AWS_ACCESS_KEY_ID= <SUA_ACCESS_KEY>

export AWS_SECRET_ACCESS_KEY= <SUA_SECRET_ACCESS_KEY>

```

Now, go back to your working directory and run the following command:

`source ~/.bashrc`

You will also need to place these keys in another document. Again, navigate to the root directory and look for the `.aws` folder. Access it via the terminal and create a file named `credentials`, with the command below:

`touch credentials`

Next, edit the file with:

`nano credentials`

Add the following lines:

```[default]
aws_access_key_id=<sua_access_key>
aws_secret_access_key=<sua_secret_access_key>
```

#### WARNING :warning: :no_entry_sign: : DO NOT PUBLISH THESE KEYS UNDER ANY CIRCUMSTANCES.


### Checking Permissions

With everything set up, ensure your user has administrative permissions, which will allow you to create, list, and delete resources in different regions. To do this, access the console:


![WhatsApp Image 2022-11-24 at 21 33 51](https://user-images.githubusercontent.com/62647438/203878313-dad61a6c-53d3-435f-93c4-2c3bdfe6cb81.jpeg)


Then, go to the IAM section and find your user. Click on it and check if you have administrative permission, as shown below:


![WhatsApp Image 2022-11-24 at 21 33 35](https://user-images.githubusercontent.com/62647438/203878325-547cab91-aa01-4bd3-b9d2-83ffd090226d.jpeg)


Now, let's proceed to the application.


## Starting with the Application :computer:


After installing and configuring everything necessary, you can clone this repository. To do this, open the terminal in the folder you created and type the following command:

`git clone https://github.com/Lihsayuri/AWS-projeto-Cloud`

Navigate to the `learn-terraform-aws-instance` folder and open the `main_project.py` file in your favorite code editor (I recommend using VsCode).

Then, simply run the code and follow the prompts in the terminal. You should see the following screen:

![WhatsApp Image 2022-11-24 at 21 36 40](https://user-images.githubusercontent.com/62647438/203878531-235f3c0e-8a71-4a97-aa30-ba5ccb7db613.jpeg)


You can choose from the following options in the menu:

        
    0 - Manual de uso da aplicação/ User manual for the application; ; 
    1 - Iniciar uma instância existente/ Start an existing instance;
    2 - Parar uma instância existente/ Stop an existing instance;
    3 - Criar uma nova instância e security groups/ Create a new instance and security groups;
    4 - Destruir algum recurso/ Destroy a resource;
    5 - Listar recursos/ List resources;
    6 - Criar um usuário/ Create a user; 
    7 - Aplicar todas alterações feitas em uma região/ Apply all changes made in a region;
    8 - Mudar a região onde você está trabalhando/ Change the region you are working in;
    9 - Sair do programa/ Exit the program


Simply select one of these options, and the program will take care of the rest. It is recommended to read the manual before selecting any other options.


## User Manual :bookmark_tabs: :

Portuguese version:

    Bem-vindo ao manual de uso da aplicação de criação de recursos na AWS.
    
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

English version:

    Welcome to the user manual for the AWS resource creation application.

    The application was developed to facilitate the creation of instances in AWS, with the ability to create instances with different security configurations (security groups) that have different rules.
    With this application, you will be able to:

    - Create instances with a name, machine image, and host type.
    - Create security groups and associate them with these machines.
    - Create security rules for the security groups.
    - Create a user with access permissions to AWS resources.
    - List created resources, such as instances, security groups, their rules, and users.
    - Delete instances, security groups, security group rules, and users (that you created).
        
    Note for this application:
    
    - You must have Python 3.8.5 or higher installed.
    - You must have Terraform 0.14.5 or higher installed.
    - You must have AWS CLI 2.1.19 or higher installed.
    - You must have Boto3 1.17.19 or higher installed.
    - You must have JSON 2.0.9 or higher installed.
    - You must have OS 1.0.1 or higher installed.

    Usage notes for the application:
    
    - You must have an AWS account.
    - You must have a user with permissions to access AWS resources.
    - You should place your user credentials in the ~/.bashrc file or another file that loads environment variables. Simply add the following lines to the file:

        export AWS_ACCESS_KEY_ID = SUA_ACCESS_KEY_ID"
        export AWS_SECRET_ACCESS_KEY = "SUA_SECRET_ACCESS_KEY"        

        Then run the command: source ~/.bashrc or another depending on the file you placed the environment variables in.

    Notes on resource management:
    - You cannot completely delete the security group of an instance. Therefore, if you choose this option, all rules (except for the default rule that comes with the instance creation in AWS) will be deleted.
    - The restrictions you will apply to the user are predefined to facilitate your configuration.
    - Changes will only be made if you select the option to apply changes.
    - To access the user's password and use the AWS console, you must first select the option to apply the changes. After applying, the output of the program will provide information about the created users, including 10-digit passwords.


## Code Construction  :construction_worker: :computer:

In general, the application code was built in the `main_project.py` file through a main function: `main()`, which calls several other functions according to the user's responses. This application has a main loop that is responsible for continuously loading the menu until the user requests to exit (or if an error occurs that unfortunately has not been handled; in that case, just run the application and try again :) ). From this loop, other functions are called and write all user responses to a variables file in JSON format (as it is easier to manipulate together with Python).

These variables will be populated in the code blocks of the Terraform files. Thus, the structure and connection between Python and Terraform can be described as follows:

- Python retains the user information and uses it to write a variable file in JSON format.
- This JSON file is interpreted by Terraform as the input values for the variables defined in the `variables.tf` file. 
- Each variable in the `variables.tf` file can be referenced by other Terraform files (which are code blocks creating resources and capturing important information) through a var.(variable_name) citation.
- Therefore, the sequence is: information flows from Python to the JSON file, this JSON file provides input values for the variables declared in `variables.tf`, and these variables are filled in the Terraform files in a dynamic way — meaning they can change, they will not always be the same (unless the user always requests the same things).

It is worth noting that in the Python program, several checks were made regarding the user's responses, such as checks for some answers but not for all. Therefore, **make sure to answer exactly what is being asked**.

Moreover, it is important to highlight that the goal is to automate and simplify the use of AWS through Terraform, many resources are indeed predefined. For example, if the user wishes to impose certain restrictions when creating other users, they can choose from three restriction options: read-only, read and create, or read, create, and delete.


## Code Construction Details

## Main Terraform Files

At this point, you should understand that Terraform is responsible for provisioning all the necessary resources to build the infrastructure. But how? Well, as mentioned before, Terraform has a declarative language and each code block has a function. Among them, we have: resources, data, and outputs. The `resources` are responsible for describing the resources to be created, while `data` represents data that can be used by Terraform even if it has been defined outside of it, and `outputs` are data returned by Terraform itself that inform about your infrastructure.

So how are these blocks organized? For each region — in this case, we are using only `us-east-1` and `us-west-1` - each infrastructure is made up of the following Terraform files: `main.tf`, `instances.tf`, `sec_group`, `autoscaling.tf`, `data.tf` e `output.tf`. They are structured as follows:

- main.tf: It is in main that the basic resources such as our provider, region, VPC, subnets, and gateway are provisioned. From this basic structure, it will be possible to create instances and security groups and their rules. Remember: your virtual private cloud is within a region and has subnets where instances will be created.

- instances.tf : This document is where instances are created and where security groups are associated.

- sec_group.tf: This document is where security groups and their rules are created.

- autoscaling.tf: This document is where the Load Balancer, Auto-Scaling Group, and the configuration to start a new instance are set up.

For example, here’s a snippet from the `main.tf` code below:

``` terraform 
resource "aws_vpc" "main" {
  cidr_block       =    var.vpc_cidr_block 
  instance_tenancy = "default"

  tags = {
    name = "VPC_certa${var.aws_region}"
  }
}
```

Remember that I mentioned `var.[variable_name]`? You will understand the importance of this argument.


## Variables in the Project

That’s why the `variables.tf` file exists. In it, all variables that will be used dynamically were declared, meaning those that are not always fixed and that the user has the power of choice. But this document only declares the format of the variables as you can see below:

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

The variables themselves come from another file: .auto.tfvars.json (which changes its name slightly depending on the region). It is here that the user inputs will be inserted, and from there the variables declared in `variables.tf` will pull the information. And with them correctly defined, you just need to call the `var`. argument plus the variable name of interest for these dynamically configured values to be filled in the `resources` blocks in the other Terraform files.

To give you a better view of this `.json` file, an example can be seen below:


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

But what if I want to create multiple resources at once? This is where the `for_each` function comes in, which can iterate over lists, maps, and objects to define a variable with multiple values — enabling the creation of multiple instances, security groups, and users. An example of it in action can be seen below:

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

## Regions, VPCs and Subnets

As mentioned earlier, we are working with only 2 regions, and this was done through Python, which switches folders depending on the region the user chooses — either `us-east-1` or `us-west-1`. Thus, everything the user deploys in one region will remain in that region — likewise, everything they destroy in that region will only be destroyed there.

Additionally, within each region, there is a VPC with fixed IP values that cannot be changed by the user: in the case of the `us-east-1` region, the CIDR block is `10.0.0.0/16`, and in the `us-west-1` region, this block changes to `172.16.0.0/16`. Finally, the subnets are located within each of these VPCs and are also determined based on the IP range of the VPC.

### Users

To create users, a separate folder was created with resources and data specifically for this purpose because, regardless of the accessed region, the users remain the same. Thus, as the project was structured, the user resources are included in the `iam.tf` document, and their data and outputs are found in `data.tf` and `output.tf`, respectively (all these documents are within the `terraform-users` folder).

Every time you create a user and apply the changes, the output will show you the access password and the AWS console access information for that created user.

### High Availability

Finally, high availability has been implemented for web servers in the us-east-1 region. When an instance created from my image is launched, if its CPU usage reaches an average of 50%, a new instance will be created in about 2 minutes. If this occurs again, another instance will be launched — this is because I configured a maximum of 3 instances to meet the application's needs. Furthermore, if after 2 minutes the average usage is below 10%, those instances will be shut down. This can be tested with a stress test that can be executed with the following command after accessing the instance via SSH:

`stress --cpu 8 --timeout 300`

This is possible because the load balancer points to a group — the target group — which is defined with the instances. Thus, through alarms that will monitor CPU usage, when the threshold is reached (both above and below), it will execute a configured policy that will create or shut down instances. When created, it will use an image template created by me that already has a simple web-server application for testing — which will always be executed when the instance is accessed (this was done via the `crontab` command) — and already has the `stress` module installed. Remember that the correct ports have been opened for each resource to allow access to the application and SSH.

**Note: the test takes a little time, but it is functioning :) and this was implemented only for the us-east-1 region in the `autoscaling.tf` file** 


## Final Notes :bookmark:

Make good use of the application, and if you use anything from here, please reference the repository. For any questions about the code or the application, please contact  @Lihsayuri.

## References:

- Terraform (documentation and code examples);
- Class outlines and professors: Rodolfo Avelino and Tiago Demay.

