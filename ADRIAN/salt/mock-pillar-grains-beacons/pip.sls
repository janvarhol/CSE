easy_install_pip:
  cmd.run:
    - name: |
        easy_install-2.7 pip
    - unless:
      - pip
    - hide_output: True
    - reload_modules: True
