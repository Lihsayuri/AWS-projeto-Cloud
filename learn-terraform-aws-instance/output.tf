output "password" {
//    sensitive = true
    value     = aws_iam_user_login_profile.profile.encrypted_password
}


output "nome_instancia_region" {
    value = [for key, value in aws_instance.app_server : "${key} - ${value.availability_zone}"]
  
}

output "instances" {
    value = data.aws_instances.instances
}

output "sec_group_name" {
    value = aws_security_group.allow.name
}

output "sg_ingress_rules" {
    value = var.sg_ingress_rules
}


output "aws_iam_users" {
    value = data.aws_iam_users.users
}
  


# encrypted_password

    