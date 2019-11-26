##
# Clean up the minion - remove salt, cert/key, and stop minion

remove_nm_iface:
  module.run:
    - name: nmcli.delete_connection
    - connection_id: wired-ebay-corp

remove_pki_dir:
  file.absent:
    - name: /etc/pki/salt

disable_minion:
  service.disabled:
    - name: salt-minion

remove_minion:
  pkg.purged:
    - name: salt-minion

# TODO
# remove /var/cache/salt
# determine if other files/folders need to be removed
# remove qualys (and license), others?
