# install pip
#python-pip:
#  pkg.installed
include:
  - mock-pillar-grains-beacons.pip

pip_install_pyinotify:
  pip.installed:
    - name: pyinotify
    - require:
      - cmd: easy_install_pip # from included pip state
    - reload_modules: True
