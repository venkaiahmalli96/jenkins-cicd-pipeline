output "jenkins_server_public_ip" {
  description = "Public IP of the Jenkins server"
  value       = aws_instance.jenkins_server.public_ip
}

output "jenkins_url" {
  description = "Jenkins Web UI URL"
  value       = "http://${aws_instance.jenkins_server.public_ip}:8080"
}

output "flask_app_url" {
  description = "Flask application URL"
  value       = "http://${aws_instance.jenkins_server.public_ip}:5000"
}

output "ssh_command" {
  description = "SSH command to connect to Jenkins server"
  value       = "ssh -i ~/.ssh/id_rsa ec2-user@${aws_instance.jenkins_server.public_ip}"
}

output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.jenkins_server.id
}
