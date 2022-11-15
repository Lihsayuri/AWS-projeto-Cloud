
resource "aws_iam_group" "group" {
    name       = "Alunos"
    path       = "/users/"  
}

resource "aws_iam_user" "user" {
  name = var.aws_user_name
  # path = "/system/"

  tags = {
    tag-key = "created-user"
  }
}

resource "aws_iam_access_key" "user" {
  user = aws_iam_user.user.name
}

resource "aws_iam_user_login_profile" "profile" {
  user                    =  aws_iam_user.user.name
  pgp_key                 =  var.pgp_key
  password_reset_required =  true
  password_length         =  10  
}

resource "aws_iam_user_group_membership" "add_user" {
    user         =  aws_iam_user.user.name                           
    groups = [aws_iam_group.group.name]
    depends_on = [aws_iam_user.user]
}


resource "aws_iam_policy" "start_stop" {
  name        = "StartStopInstances"
  path        = "/"
  description = "Permite user iniciar e parar instancias"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            "Sid": "FirstStatement",
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "arn:aws:ec2:*:116979769772:instance/*"
        },
        {
            "Sid": "SecondStatement",
            "Effect": "Allow",
            "Action": "ec2:DescribeInstances",
            "Resource": "*"
        }
    ]
  })
}


resource "aws_iam_policy" "change_pass" {
  name        = "ChangePassword"
  path        = "/"
  description = "Permite user trocar senha"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
        {
            "Sid": "FirstStatement",
            "Effect": "Allow",
            "Action": "iam:ChangePassword",
            "Resource": "arn:aws:iam::116979769772:user/*"
        }
    ]

    
  })
}

resource "aws_iam_policy" "niveis" {
  name        = var.policy_name
  path        = "/"
  description = var.policy_description

  policy = jsonencode({
    "Version" = "2012-10-17"
    "Statement" = [
        {
            "Effect" = var.policy_effect
            "Action" = var.policy_action
            "Resource" = var.policy_resource
        }
    ]
})
}



resource "aws_iam_policy_attachment" "attach" {
    name       = "EC2StartStopOwnInstances"
    groups     = [aws_iam_group.group.name]
    # policy_arn = data.aws_iam_policy.StartI.arn
    policy_arn = aws_iam_policy.start_stop.arn

}

resource "aws_iam_policy_attachment" "attach2" {
    name       = "ChangePass"
    groups     = [aws_iam_group.group.name]
    # policy_arn = data.aws_iam_policy.ChangePass.arn
    policy_arn = aws_iam_policy.change_pass.arn

}


resource "aws_iam_policy_attachment" "attach3" {
    name       = var.policy_name
    groups     = [aws_iam_group.group.name]
    # policy_arn = data.aws_iam_policy.ChangePass.arn
    policy_arn = aws_iam_policy.niveis.arn

}



## POLÍTICAS EM NÍVEIS:

# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": [
#         "ec2:Describe*",
#         "ec2:Get*",
#         "ec2:Create*"
#       ],
#       "Effect": "Allow",
#       "Resource": "*"
#     }
#   ]
# }

# {
#     "Version" : "2012-10-17",
#     "Statement" : [
#       {
#         "Action": [
#           "ec2:Describe*",
#           "ec2:Get*"
#         ],
#         "Effect": "Allow",
#         "Resource": "*"
#       }
#     ]    
#   }



# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": [
#         "ec2:Describe*",
#         "ec2:Get*",
#         "ec2:Create*",
#         "ec2:Delete*"
#       ],
#       "Effect": "Allow",
#       "Resource": "*"
#     }
#   ]
# }


# resource "aws_iam_user_policy" "user_ro" {
#   name = "test"
#   user = aws_iam_user.user.name

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": [
#         "ec2:Describe*",
#         "ec2:Stop*",
#         "ec2:Start*"
#       ],
#       "Effect": "Allow",
#       "Resource": "*"
#     }
#   ]
# }
# EOF
# }

# outputs for arn
# output "user_arn" {
#   value = "${aws_iam_user.user.arn}"
# }