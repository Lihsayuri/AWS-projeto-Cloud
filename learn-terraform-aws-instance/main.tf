# VPC criação de uma VPC e sub-rede; instâncias: esta funcionalidade deverá permitir a escolha de pelo menos 2 tipos de configuração de hosts;
# ainda deverá ser possível parar e iniciar as instâncias; security group: criação e a associação de grupos de segurança com instâncias; Usuário no IAM.


terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

# Prover as credenciais da AWS
provider "aws" {
  region = var.aws_region
}
   

resource "aws_vpc" "main" {
  cidr_block       = "10.0.0.0/16"
  instance_tenancy = "default"

  tags = {
    Name = "VPC"
  }
}

resource "aws_subnet" "main" {
  vpc_id     = aws_vpc.main.id
  cidr_block = "10.0.1.0/24"

  tags = {
    Name = "Subnet"
  }
}

# resource "aws_subnet" "private" {
#   cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, 1)
#   availability_zone       = data.aws_availability_zones.available.names[0]
#   vpc_id                  = aws_vpc.main.id
#   map_public_ip_on_launch = true

#   tags = {
#     Name = "Private"
#   }
#   depends_on = [aws_internet_gateway.gw]
# }



# resource "aws_subnet" "public" {
#   cidr_block              = cidrsubnet(aws_vpc.main.cidr_block, 8, 2)
#   availability_zone       = data.aws_availability_zones.available.names[1]
#   vpc_id                  = aws_vpc.main.id
#   map_public_ip_on_launch = true

#   tags = {
#     Name = "Public"
#   }
# }




## ESSE TAVA CERTO
# resource "aws_security_group" "allow_tls" {
#   name        = var.security_group_name
#   description = "Grupo de seguranca para a instancia"
#   vpc_id      = aws_vpc.main.id
    
#     ingress {
#         description = var.description_security_group
#         from_port   = var.aws_from_port
#         to_port     = var.aws_to_port
#         protocol    = var.aws_protocol
#         cidr_blocks = var.aws_cidr_blocks
#     } 


#     egress {
#         from_port   = 0
#         to_port     = 0
#         protocol    = "-1"
#         cidr_blocks = ["0.0.0.0/0"]
#     }
#     tags = {
#         name        = "security_group"
#     }
#     depends_on      = [aws_vpc.main]
  
# }


### O DE CIMA TAVA CERTO

# resource "aws_security_group" "allow_tls" {
#   name        = var.security_group_name
#   description = "Grupo de segurança para a instância"
#   vpc_id      = aws_vpc.main.id

#   ingress  = var.aws_ingress
#   # ingress {
#   #   description      = "SSH"
#   #   from_port        = 443
#   #   to_port          = 443
#   #   protocol         = "tcp"
#   #   cidr_blocks      = [aws_vpc.main.cidr_block]
#   #   ipv6_cidr_blocks = [aws_vpc.main.ipv6_cidr_block]
#   # }

#   egress {
#     from_port        = 0
#     to_port          = 0
#     protocol         = "-1"
#     cidr_blocks      = ["0.0.0.0/0"]
#     ipv6_cidr_blocks = ["::/0"]
#   }

#   tags = {
#     Name = "allow_tls"
#   }
# }

# {description = "criando security group para teste", from_port = 443, to_port = 443, protocol = "tcp", cidr_blocks = ["10.0.0.0/16"]}


# aws_region = "us-east-1"
# image_id = "ami-0149b2da6ceec4bb0"
# aws_instance_type = "t2.micro"
# aws_user_name = "teste"
# security_group_name = "seguranca teste"
# description_security_group = "SSH"
# aws_from_port = 22
# aws_to_port = 22
# aws_protocol = "tcp"
# aws_cidr_blocks = ["0.0.0.0/0"] 
# i-063acc0097b42b925
