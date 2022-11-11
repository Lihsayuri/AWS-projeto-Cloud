data "aws_iam_policy" "StartI" {
    arn = "arn:aws:iam::116979769772:policy/EC2StartStopInstances"
}

data "aws_iam_policy" "ChangePass" {
    arn = "arn:aws:iam::116979769772:policy/IAM_ACESS"  
}