# Orchestration state to run a compliance check on known minion
{% set minion_id = salt.pillar.get('minion_id') %}

{# AM: BLOCK REMOVED FOR TESTING
{% set exception = salt.pillar.get('exception') %}
{% set minion_macs = salt['lampapi.get_minion_macs'](minion_id) %}
{# {% set minion_data = salt.lampapi.get_minion(minion_id) %} #}
{# {% set scan_date = salt.lampapi.get_last_update(minion_id) %} #}
{# {% set master = salt.pillar.get('master_id') %}
{% set exceptions = salt['ebay_exceptions.load'](minion_id) %}
#}
# AM: BLOCK ADDED FOR TESTING
{% set minion_data = {'include_scan': True} %}
{% set exceptions = [] %}
{% set master = 'ebay' %}
# END


{% load_yaml as checks %}
# minion.password_check modified with test.configurable_test_state to fix return to True/False
- name: password_check
  fail_reason: password check failure for local root account
  sls: minion.password_check
  msg_admin: True
  pillar:
      username: root

# luks state modified with test.configurable_test_state to return to fix return to True/False
- name: luks_check
  fail_reason: minion is not encrypted properly with LUKS
  sls: luks # ---->>>> Krushna: CHECK IF THIS SHOULD BE minion.luks_check (minion/luks_check.sls)
  msg_admin: True

{% endload %}

{% if not minion_id %}
fail_hard:
  test.fail_without_changes:
    - name: Must have a 'minion_id' passed as a pillar
    - failhard: True
{% endif %}

# TODO consider wrapping these states inside a single prep_compliance.sls file
# START
test_connected:
  salt.function:
    - tgt: {{ minion_id }}
    - name: test.ping
    - failhard: True

sync_modules:
  salt.function:
    - tgt: {{ minion_id }}
    - name: saltutil.sync_all
# END


{% if 'include_scan' in minion_data and minion_data.include_scan %}
#install_schedules:
#  salt.state:
#    - tgt: {{ minion_id }}
#    - sls:
#      - minion.schedule
#    - queue: True

# install_schedules modified with test.configurable_test_state to return to fix return to True/False
install_schedules:
  test.configurable_test_state:
    - name: SIMULATED INSTALL SCHEDULES
    - changes: False
    - result: True

# Get minion osfinger
{% set minion_grains = salt.saltutil.runner(name='salt.execute', arg=[minion_id, 'grains.items']) %}
{% set minion_osfinger = minion_grains[minion_id]['osfinger'] %}

# List of executed checks
{% set run_checks_list = [] %}

# ITERATE THRU CHECKS
{% for check in checks %}
# Establish whether exception based on check info is required
# Ex: Skip disk encryption check and wifi encryption check for Raspbian devices
{% set except_this_raspbian = false %}
{% set exclude_checks = ['luks_check', 'qualys_scan_check'] %}
{% if check.name in exclude_checks and minion_osfinger.startswith('Raspbian') %}
{% set except_this_raspbian = true %}
{% endif %}

{% if (check.name not in exceptions) and not except_this_raspbian %}

# Add check to run_checks_list
{% do run_checks_list.append(check.name) %}

{{ check.name }}:
  salt.state:
    - tgt: {{ minion_id }}
    - sls:
        - {{ check.sls }}
    - queue: True
    {% if check.get('pillar') %}
    - pillar: {{ check.pillar|yaml }}
    {% endif %}
    - require_in:
      - update_success

set_compliant_all_false_{{check.name}}:
  salt.function:
    - tgt: {{ minion_id}}
    - name: "grains.set"
    - arg:
      - "compliant:all"
      - False
    - onfail:
      - {{ check.name }}

set_compliance_false_{{check.name}}:
  salt.function:
    - tgt: {{ minion_id}}
    - name: "grains.set"
    - arg:
      - "compliant:{{check.name}}"
      - False
    - onfail:
      - {{ check.name }}

set_compliance_grain_True_{{check.name}}:
  salt.function:
    - tgt: {{ minion_id}}
    - name: "grains.set"
    - arg:
      - "compliant:{{check.name}}"
      - True
    - require:
      - {{ check.name }}

set_compliance_exception_grain_False_{{check.name}}:
  salt.function:
    - tgt: {{ minion_id}}
    - name: "grains.set"
    - arg:
      - "compliant:exception:{{check.name}}"
      - False

{#{% if salt['date_compare.is_today'](scan_date) %}#}

{{ check.name }}_fail:
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      - master.compliance_fail
{#
    - pillar:
        minion_id: {{ minion_id }}
        reason: {{ check.fail_reason }}
        email: {{ minion_data.email }}
        name: {{ minion_data.name }}
        description: {{ minion_data.description }}
        num_fails: '{{ minion_data.num_fails }}'
        mac: {{ minion_macs.macs[0] }}
        msg_admin: {{ check.msg_admin }}
#}
    - failhard: True
    - onfail:
      - {{ check.name }}

{#{% endif %}#}

{% else %}
# Set exception to true
set_compliance_exception_grain_True_{{check.name}}:
  salt.function:
    - tgt: {{ minion_id}}
    - name: "grains.set"
    - arg:
      - "compliant:exception:{{check.name}}"
      - True

{% endif %}
{% endfor %}

update_success:
  salt.state:
    - sls: master.compliance_success
    - tgt: {{ master }}
    - concurrent: True
    - pillar:
        minion_id: {{ minion_id }}

set_compliant_all_true:
  salt.function:
    - tgt: {{ minion_id}}
    - name: "grains.set"
    - arg:
      - "compliant:all"
      - True
    - require:
      - update_success


check_connection:
  salt.state:
    - tgt: {{ minion_id }}
    - sls: minion.check_connection
    - queue: True
    - require:
      {% for check in run_checks_list %}
      - {{ check }}
      {% endfor %}

lamp_check_cert_valid:
# AM: STATE MODIFIED FOR TESTING
  test.configurable_test_state:
    - name: checking_valid_cert
{#    - result: {{minion_data.cert_valid}} #}
    - result: True
    - changes: False
    - require:
      {% for check in run_checks_list %}
      - {{ check }}
      {% endfor %}

gen_csr_for_minion:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.state:
    - tgt: {{ minion_id }}
    - queue: True
    - sls:
      - cert.gen_csr
#}
  test.configurable_test_state:
    - name: SIMULATED gen_csr_for_minion
    - changes: False
    - result: True
    - onfail_any:
      - check_connection
      - lamp_check_cert_valid
    - require:
      {% for check in run_checks_list %}
      - {{ check }}
      {% endfor %}

gen_request_for_minion:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      - cert.gen_request
    - pillar:
        minion_id: {{ minion_id }}
#}
  test.configurable_test_state:
    - name: SIMULATED gen_request_for_minion
    - changes: False
    - result: True
    - require:
      - gen_csr_for_minion
    - onfail_any:
      - check_connection
      - lamp_check_cert_valid
    - timeout: 180

get_cert_for_minion:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      - cert.get_cert
    - pillar:
        minion_id: {{ minion_id }}
#}
  test.configurable_test_state:
    - name: SIMULATED get_cert_for_minion
    - changes: False
    - result: True
    - require:
      - gen_request_for_minion
    - onfail_any:
      - check_connection
      - lamp_check_cert_valid
    - timeout: 180

add_cert_in_db:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      - cert.record_cert
    - pillar:
        minion_id: {{ minion_id }}
#}
  test.configurable_test_state:
    - name: SIMULATED add_cert_in_db
    - changes: False
    - result: True
    - onfail_any:
      - check_connection
      - lamp_check_cert_valid
    - require:
        - get_cert_for_minion

deploy_cert_for_minion:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.state:
    - tgt: {{ minion_id }}
    - queue: True
    - sls:
      - cert.deploy_crt
#}
  test.configurable_test_state:
    - name: SIMULATED deploy_cert_for_minion
    - changes: False
    - result: True
    - require:
      - add_cert_in_db
    - onfail_any:
      - check_connection
      - lamp_check_cert_valid
    - timeout: 180

manage_nm:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.state:
    - tgt: {{ minion_id }}
    - queue: True
    - sls:
      - minion.manage_nm
    - pillar:
        mac: {{ minion_macs.macs[0] }}
#}
  test.configurable_test_state:
    - name: SIMULATED manage_nm
    - changes: False
    - result: True
    - require:
        - update_success

manage_nm_fail:
  salt.state:
    - tgt: {{ master }}
    - concurrent: True
    - sls:
      # master.nm_fail modified for testing
      - master.nm_fail
# AM: STATE MODIFIED FOR TESTING
{#
    - pillar:
        minion_id: {{ minion_id }}
        reason: Network Configuration Failure
        email: {{ minion_data.email }}
        name: {{ minion_data.name }}
        description: {{ minion_data.description }}
        num_fails: '{{ minion_data.num_fails }}'
        mac: {{ minion_macs.macs[0] }}
#}
#    - failhard: True
    - onfail:
      - manage_nm


move_to_eBay_Linux_Provisioned:
# AM: STATE MODIFIED FOR TESTING
{#
  salt.function:
    - tgt: {{ master }}
    - name: ise.assign_group
    - kwarg:
        group: eBay_Linux_Provisioned
        mac: {{ minion_macs.macs[0] }}
#}
  test.configurable_test_state:
    - name: SIMULATED move_to_eBay_Linux_Provisioned
    - changes: False
    - result: True
    - require:
        - manage_nm


{% else %}
do_not_run:
  test.succeed_without_changes:
    - name: {{ minion_id }} not included in scans
{% endif %}
