output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.dc_dashboard.id
}

output "public_ip" {
  description = "Elastic IP — your stable dashboard address"
  value       = aws_eip.dc_dashboard.public_ip
}

output "dashboard_url" {
  description = "Direct URL to the Streamlit dashboard"
  value       = "http://${aws_eip.dc_dashboard.public_ip}:8501"
}

output "ssh_command" {
  description = "SSH command to log into the instance"
  value       = "ssh -i ${replace(var.public_key_path, ".pub", "")} ec2-user@${aws_eip.dc_dashboard.public_ip}"
}
