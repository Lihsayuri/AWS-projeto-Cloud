# resource "aws_launch_configuration" "web" {
#     name_prefix = "web-"
#     image_id = "ami-08dc32339a1415ca1" #isso aqui que tem que mudar
#     instance_type = "t2.micro"
#     key_name = "livia"
#     security_groups = [ "${aws_security_group.demosg1.id}" ]
#     associate_public_ip_address = true
#     # user_data = "${file("data.sh")}"
#     lifecycle {
#         create_before_destroy = true
#     }
# }