{% do salt.log.debug('LOGGING ORCHESTRATION INFO...') %}
do logging:
  test.succeed_without_changes
