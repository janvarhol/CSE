[802-3-ethernet]
duplex=full
 
[connection]
id=wired-ebay-corp
uuid={{ uuid }}
type=802-3-ethernet
 
[ipv6]
method=auto
 
[802-1x]
eap=tls;
identity=host/{{ grains.fqdn }}
client-cert=/etc/pki/salt/802.1x.crt
private-key=/etc/pki/salt/{{ grains.id }}.key
private-key-password-flags=0
private-key-password={{ pillar.get('nm_key_pass') }}

[ipv4]
method=auto

