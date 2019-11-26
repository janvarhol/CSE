simple_test1:
  salt.function:
    - name: test.ping
    - tgt: cmaster01
