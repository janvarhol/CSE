# Fail if we are missing pillar
fail_if-missing_pillar:
  test.check_pillar:
    - present:
      - ActivationId
      - CustomerId
    - failhard: True

{% set sources = salt['grains.filter_by']({
  'RedHat': { 'package': 'qualys-cloud-agent.x86_64.rpm' },
  'Fedora': { 'package': 'qualys-cloud-agent.x86_64.rpm' },
  'Centos': { 'package': 'qualys-cloud-agent.x86_64.rpm' },
  'Debian': { 'package': 'qualys-cloud-agent.x86_64.deb' },
  'Ubuntu': { 'package': 'qualys-cloud-agent.x86_64.deb' },
  'Raspbian': { 'package': 'qualys-cloud-agent.x86_64.deb' }
}) %}

{% set qualys_installed  = salt.pkg.version('qualys-cloud-agent') %}

check-scanner-installed:
  test.configurable_test_state:
    - name: qualys_installed state
    - result: True
    - changes: {{ qualys_installed == None }}

message_invalid_os_for_qualys:
  test.configurable_test_state:
    - name: qualys_unsupported_os
    {% if sources.get('package', False) %}
    - result: True
    {% endif %}
    - changes: False
    - failhard: True

# Use pkg.installed instead of module.run
qualys-cloud-agent-install:
  pkg.installed:
    - sources:
      - qualys-cloud-agent: salt://minion/files/{{ sources.package }}
    - onchange:
      - check-scanner-installed

# TODO: How confident are we in this executable path across os versions?
qualys-cloud-agent-deploy:
  cmd.script:
    - name: /usr/local/qualys/cloud-agent/bin/qualys-cloud-agent.sh
    - args: "'ActivationId={{ salt['pillar.get']('ActivationId') }}' 'CustomerId={{ salt['pillar.get']('CustomerId') }}'"
    # TODO we should only run this when needed
    - onchange:
      - check-scanner-installed

# the agent deploy takes time asynchronously to finish
test_sleep_60:
  module.run:
    - name: test.sleep
    - length: 15
    - onchange: 
      - qualys-cloud-agent-deploy

check-scanner-service:
  service.running:
    - name: qualys-cloud-agent
    - enable: True
    - restart: True
    - require:
      - test_sleep_60
    - watch:
      - qualys-cloud-agent-install
