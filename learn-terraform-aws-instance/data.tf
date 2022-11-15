data "aws_iam_policy" "StartI" {
    arn = "arn:aws:iam::116979769772:policy/EC2StartStopInstances"
}

data "aws_iam_policy" "ChangePass" {
    arn = "arn:aws:iam::116979769772:policy/IAM_ACESS"  
}

data "aws_iam_users" "users" {}

data "aws_instances" "instances" {
  instance_state_names = ["running", "stopped"]

  # Pegue a tag Name de cada instância
}




# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "VisualEditor0",
#             "Effect": "Allow",
#             "Action": [
#                 "ec2:StartInstances",
#                 "ec2:StopInstances"
#             ],
#             "Resource": "arn:aws:ec2:*:116979769772:instance/*"
#         },
#         {
#             "Sid": "FirstStatement",
#             "Effect": "Allow",
#             "Action": "ec2:DescribeInstances",
#             "Resource": "*"
#         }
#     ]
# }

# START STOP INSTANCES


# {
#     "Version": "2012-10-17",
#     "Statement": [
#         {
#             "Sid": "FirstStatement",
#             "Effect": "Allow",
#             "Action": "iam:ChangePassword",
#             "Resource": "arn:aws:iam::116979769772:user/*"
#         }
#     ]
# }
# CHANGE PASSWORD


# GET AND LIST:

# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Sid": "FirstStatement",
#       "Effect": "Allow",
#       "Action": "s3:ListAllMyBuckets",
#       "Resource": "*"
#     },
#     {
#       "Sid": "SecondStatement",
#       "Effect": "Allow",
#       "Action": [
#         "s3:List*",
#         "s3:Get*"
#       ],
#       "Resource": [
#         "arn:aws:s3:::confidential-data",
#         "arn:aws:s3:::confidential-data/*"
#       ],
#       "Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}}
#     }
#   ]
# }