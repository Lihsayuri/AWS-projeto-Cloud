
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

resource "aws_iam_policy_attachment" "attach" {
    name       = "EC2StartStopOwnInstances"
    groups     = [aws_iam_group.group.name]
    policy_arn = data.aws_iam_policy.StartI.arn

}

resource "aws_iam_policy_attachment" "attach2" {
    name       = "ChangePass"
    groups     = [aws_iam_group.group.name]
    policy_arn = data.aws_iam_policy.ChangePass.arn

}


















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