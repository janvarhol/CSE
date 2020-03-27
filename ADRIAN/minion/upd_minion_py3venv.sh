#!/bin/bash
yum install -y gcc python3
yum --enablerepo=* install -y rh-python36
yum --enablerepo=* install -y rh-python36-python-devel
yum --enablerepo=* install -y rh-python36-python-virtualenv
yum --enablerepo=* install -y python3-devel
python3 -m pip install --upgrade pip
pip3 install virtualenv
python3 -m venv /opt/saltstack/salt/venv
/opt/saltstack/salt/venv/bin/pip3.6 install salt==3000
cp /etc/systemd/system/multi-user.target.wants/salt-minion.service /etc/systemd/system/salt-minion.service
systemctl stop salt-minion
yum remove salt-minion -y
sed -i 's/ExecStart.*/ExecStart=\/opt\/saltstack\/salt\/venv\/bin\/salt-minion/' /etc/systemd/system/salt-minion.service
systemctl daemon-reload
systemctl enable salt-minion
systemctl start salt-minion


# salt minion-201920 cp.get_file salt://upd_minion_py3venv.sh /tmp/upd_minion_py3venv.sh
# salt minion-201920 cmd.run 'chmod +x /tmp/upd_minion_py3venv.sh'
# salt minion-201920 cmd.run_bg '/tmp/upd_minion_py3venv.sh'
