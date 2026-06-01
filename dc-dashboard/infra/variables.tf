variable "aws_region" {
  description = "AWS region to deploy into"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Name tag applied to every resource"
  type        = string
  default     = "dc-dashboard"
}

variable "instance_type" {
  description = "EC2 instance type — t2.micro is free-tier eligible"
  type        = string
  default     = "t2.micro"
}

variable "public_key_path" {
  description = "Path to your local SSH public key (e.g. ~/.ssh/id_rsa.pub)"
  type        = string
}
