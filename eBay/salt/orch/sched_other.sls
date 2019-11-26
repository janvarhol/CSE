simple_test2:
  salt.function:
    - name: cmd.run
    - tgt: cmaster01
    - arg:
      - 'ls -l /srv/salt'
