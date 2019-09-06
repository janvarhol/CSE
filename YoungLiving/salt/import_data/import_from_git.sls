{% import_json 'import_data/data_in_git.json' as some_data %}

Show_entire_json_dict:
  test.configurable_test_state:
    - name: Entire dict
    - changes: False
    - result: True
    - comment: {{ some_data }}

Show_title_json_dict:
  test.configurable_test_state:
    - name: Title
    - changes: False
    - result: True
    - comment: {{ some_data['DATA IN GIT']['title'] }}
