
resource "aws_security_group" "allow" {
#   for_each = var.sec_group
  name        = var.sec_group
#   description = each.value.description
  vpc_id      = aws_vpc.main.id
    
    ingress {
        description = "All traffic"
        from_port   = 0
        to_port     = 0
        protocol    = -1
        cidr_blocks = ["0.0.0.0/0"]
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


resource aws_security_group_rule ingress {
    type        = "ingress"
    for_each = var.sg_ingress_rules
    cidr_blocks = each.value.cidr_blocks
    description = each.value.description

    from_port = each.value.from_port
    to_port   = each.value.to_port
    protocol  = each.value.protocol

    security_group_id = aws_security_group.allow.id

}


