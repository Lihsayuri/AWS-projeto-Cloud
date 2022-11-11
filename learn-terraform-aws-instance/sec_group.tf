
resource "aws_security_group" "allow" {
  for_each = var.sec_group
  name        = each.value.name
  description = "Grupo de seguranca para a instancia"
  vpc_id      = aws_vpc.main.id
    
    ingress {
        description = each.value.description
        from_port   = each.value.from_port
        to_port     = each.value.to_port
        protocol    = each.value.protocol
        cidr_blocks = each.value.cidr_blocks
    } 


    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
    tags = {
        name        = "security_group"
    }
    depends_on      = [aws_vpc.main]
  
}

