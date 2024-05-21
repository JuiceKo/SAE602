apt update

apt install -y curl openssh-server ca-certificates perl
curl https://packages.gitlab.com/install/repositories/gitlab/gitlab-ee/script.deb.sh | sudo bash
sudo EXTERNAL_URL="10.129.4.45" apt-get install gitlab-ee
