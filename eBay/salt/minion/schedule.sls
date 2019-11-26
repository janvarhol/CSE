#############################################
# This state is meant to be run on the minion
#############################################
compliance_schedule:
  schedule.present:
    - function: event.send
    - job_args:
      - 'ebay/compliance/check'
    - splay: 60
    - when:
      - Sunday 1:00pm
      - Monday 1:00pm
      - Tuesday 1:00pm
      - Wednesday 1:00pm
      - Thursday 1:00pm
      - Friday 1:00pm
      - Saturday 1:00pm

clamav_schedule:
  schedule.present:
    - function: clamav.scan
    - job_kwargs:
        directory: /home
    - when:
      - Tuesday 9:00am
