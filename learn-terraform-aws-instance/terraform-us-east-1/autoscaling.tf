
resource "aws_launch_configuration" "teste" {
  name_prefix     = "learn-terraform-aws-asg-"
  image_id        = "ami-08dc32339a1415ca1"
  instance_type   = "t2.micro"
#   user_data       = file("user-data.sh")
  security_groups = [aws_security_group.teste_instance.id]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_autoscaling_group" "teste" {
  name                 = "teste"
  min_size             = 1
  max_size             = 3
  desired_capacity     = 1
  launch_configuration = aws_launch_configuration.teste.name
  vpc_zone_identifier  = ["${aws_subnet.public.id}", "${aws_subnet.private.id}"]

  tag {
    key                 = "Name"
    value               = "HashiCorp Learn ASG - Terramino"
    propagate_at_launch = true
  }
}

resource "aws_lb" "teste" {
  name               = "learn-asg-teste-lb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.teste_lb.id]
  subnets            = ["${aws_subnet.public.id}", "${aws_subnet.private.id}"]

}

resource "aws_lb_listener" "teste" {
  load_balancer_arn = aws_lb.teste.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.teste.arn
  }
}

resource "aws_lb_target_group" "teste" {
  name     = "learn-asg-teste"
  port     = 80
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}


resource "aws_autoscaling_attachment" "teste" {
  autoscaling_group_name = aws_autoscaling_group.teste.id
  lb_target_group_arn   = aws_lb_target_group.teste.arn
}

resource "aws_security_group" "teste_instance" {
  name = "learn-asg-teste-instance"
  ingress {
    from_port       = 80
    to_port         = 80
    protocol        = "tcp"
    security_groups = [aws_security_group.teste_lb.id]
  }

  egress {
    from_port       = 0
    to_port         = 0
    protocol        = "-1"
    security_groups = [aws_security_group.teste_lb.id]
  }

  vpc_id = aws_vpc.main.id
}

resource "aws_security_group" "teste_lb" {
  name = "learn-asg-teste-lb"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  vpc_id = aws_vpc.main.id
}