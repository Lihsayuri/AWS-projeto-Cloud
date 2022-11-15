# data "aws_iam_policy" "StartI" {
#     arn = "arn:aws:iam::116979769772:policy/EC2StartStopInstances"
# }

# data "aws_iam_policy" "ChangePass" {
#     arn = "arn:aws:iam::116979769772:policy/IAM_ACESS"  
# }

data "aws_iam_users" "users" {}

data "aws_instances" "instances" {
  instance_state_names = ["running", "stopped"]

  # Pegue a tag Name de cada instância
}


