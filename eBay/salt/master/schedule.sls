#############################################
# This state is meant to be run on the master
#############################################
compliance_schedule:
  schedule.present:
    - function: state.sls
    - job_args:
      - master.stale_minions
    - when:
      - Sunday 1:00am
      - Monday 1:00am
      - Tuesday 1:00am
      - Wednesday 1:00am
      - Thursday 1:00am
      - Friday 1:00am
      - Saturday 1:00am
