{% import_yaml 'minion/clamav.map' as osmap %}
{% set clamav_data = salt['grains.filter_by'](osmap) %}

{% for clamav_pkg in clamav_data['pkgs'] %}
install_{{ clamav_pkg }}:
  pkg.installed:
    - name: {{ clamav_pkg }}
{% endfor %}
