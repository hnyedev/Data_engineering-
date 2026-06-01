terraform {
  required_version = ">= 1.3.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

locals {
  ami_id = "ami-0c02fb55956c7d316"
}

resource "aws_key_pair" "dc_dashboard" {
  key_name   = "${var.project_name}-key"
  public_key = file(var.public_key_path)
}

resource "aws_security_group" "dc_dashboard" {
  name        = "${var.project_name}-sg"
  description = "Allow SSH and Streamlit"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Streamlit"
    from_port   = 8501
    to_port     = 8501
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name    = "${var.project_name}-sg"
    Project = var.project_name
  }
}

resource "aws_instance" "dc_dashboard" {
  ami                    = local.ami_id
  instance_type          = var.instance_type
  key_name               = aws_key_pair.dc_dashboard.key_name
  vpc_security_group_ids = [aws_security_group.dc_dashboard.id]

  root_block_device {
    volume_size = 8
    volume_type = "gp2"
  }

  user_data = <<-USERDATA
    #!/bin/bash
    dnf update -y
    dnf install -y docker git
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ec2-user
  USERDATA

  tags = {
    Name    = var.project_name
    Project = var.project_name
  }
}

resource "aws_eip" "dc_dashboard" {
  instance = aws_instance.dc_dashboard.id
  domain   = "vpc"

  tags = {
    Name    = "${var.project_name}-eip"
    Project = var.project_name
  }
}
