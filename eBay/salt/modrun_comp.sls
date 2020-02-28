# Legacy Style
# salt.modules.test.arg(*args, **kwargs)
# salt-call --local test.arg "legacy style argument" "another legacy style argument" some_kwargs='{"legacy style": "yes", "testing": True}'


show_legacy_style:
  module.run:
    - name: test.arg
    - args:
      - "legacy style argument"
      - "another legacy style argument"
    - kwargs:
        some_kwargs: {"legacy_style": "yes", "testing": True}


# New style
# enable the new style in minion conf
#   use_superseded:
#     - module.run
show_new_style:
  module.run:
    - test.arg:
      - "new style argument"
      - "another legacy style argument"
      - some_kwargs: {"legacy_style": "yes", "testing": True}
