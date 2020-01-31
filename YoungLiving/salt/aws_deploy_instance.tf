# Sample Terraform template
/* This terraform template deploys:
     - Single instance
     - aws provider
*/

provider "aws" {
  access_key = "REDACTED"
  secret_key = "REDACTED"
  region     = "us-east-2"
}

resource "aws_instance" "tf-insta1" {
  ami           = "REDACTED"
  instance_type = "t2.micro"
  security_groups = ["default"]


  connection {
      type = "ssh"
      user = "root"
      password = "REDACTED"
      timeout = "2m"
      host = self.private_ip
  }

  provisioner "remote-exec" {
    inline = [
      "curl -L https://bootstrap.saltstack.com -o install_salt.sh",
      "sh install_salt.sh -P -X -A 172.31.45.90 ",
      "cat <<EOF > /etc/salt/minion.d/autosign_grains.conf",
      "autosign_grains:",
      "  - terraform_id",
      "EOF",
      "salt-call --local grains.set terraform_id 'tf_12345'",
      "systemctl stop salt-minion",
      "sleep 10; systemctl start salt-minion",
      "systemctl enable salt-minion"
     ]
   }
}
