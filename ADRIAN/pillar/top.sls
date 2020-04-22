base:
  'tsystems':
    - info
  'HPManager:isManager:True':
    - match: grain
    - mock-pillar-grains-beacons.info    # basic system info
    - mock-pillar-grains-beacons.hpmgr   # HPManager node info
    - mock-pillar-grains-beacons.beacons-inotity-grains # beacon inotify set for /etc/salt/grains
