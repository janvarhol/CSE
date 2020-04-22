beacons:
  inotify:
    - files:
        /etc/salt/grains:
          mask:
            - delete_self
            - modify
            - create
    - interval: 10 
    - disable_during_state_run: True
