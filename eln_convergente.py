from rich import print
import ipaddress
import json

print()
print("#" * 70)
print("Gerador de scripts para REDE CONVERGENTE - Eletronorte".center(70))
print("#" * 70)
print()

sites_id = {
   5: "SED",
   6: "IPZ",
   7: "COX",
   8: "TUC",
   9: "COL",
   10: "ALT",
   11: "GUA",
   12: "JIP",
   13: "LEC",
   14: "PVO",
   15: "SRB",
   16: "SLU",
   17: "TPJ",
   18: "MAR",
   19: "BCB",
   20: "PDD"
}
site_id = int(input(f"Informe o ID do Site: \n\n{json.dumps(sites_id, indent=4)}\n\n"))
print()
vlan_id = int(input(f"Informe a VLAN da Convergente: "))
print()
ce_hostname = str.upper(input(f"Informe o hostname do CE: "))
print()
pe_intf1 = str.upper(input(f"Informe a interface 1 do PO21 do Agregador (GIX/X/X): "))
print()
pe_intf2 = str.upper(input(f"Informe a interface 2 do PO21 do Agregador (GIX/X/X): "))
print()
ce_intf1 = str.upper(input(f"Informe a interface 1 do PO21 do CE (GIX/X/X): "))
print()
ce_intf2 = str.upper(input(f"Informe a interface 2 do PO21 do CE (GIX/X/X): "))
print()
ospf_area = int(input(f"Informe a area OSPF do site (decimal): "))
print()
p2p_net = str(input(f"Informe a rede P2P PE-CE (172.27.16.X/30): "))
print()

ip_lo200 = str(f"172.27.200.{site_id}")
# Verificar forma de extrair a máscara para colocar na BDI.
ip_p2p_pe = list(ipaddress.ip_network(p2p_net).hosts())[0]
ospf_rid = list(ipaddress.ip_network(p2p_net).hosts())[0]

output = f'''interface {pe_intf1}
 description CONVERGENTE-{ce_hostname}-{ce_intf1} PO21
 mtu 9202
 no ip address
 negotiation auto
 load-interval 30
 channel-group 21 mode active
 service-policy output TO_CORP
!
interface {pe_intf2}
 description CONVERGENTE-{ce_hostname}-{ce_intf2} PO21
 mtu 9202
 no ip address
 negotiation auto
 load-interval 30
 channel-group 21 mode active
 service-policy output TO_CORP
!
!
interface Port-channel21
 description TRUNK PO21 - REDE CONVERGENTE
 mtu 9202
 no ip address
 negotiation auto
 load-interval 30
 shutdown
  service instance 1 ethernet
  encapsulation untagged
  l2protocol peer lacp
  bridge-domain 1
 !
 service instance trunk 2 ethernet
  description L2 CONTROL(CDP,STP) AND L2 SWITCH
  encapsulation dot1q {vlan_id}
  rewrite ingress tag pop 1 symmetric
  l2protocol peer cdp stp
  bridge-domain from-encapsulation
  service-policy input FROM_CORP
!
interface BDI{vlan_id}
 description VRF CONVERGENTE
 ip vrf forwarding CONVERGENTE
 ip address {ip_p2p_pe} 255.255.255.252
 ip ospf 200 area 0.0.0.{ospf_area}
 shutdown
!
!
interface Loopback200
 description REDE CONVERGENTE
 ip vrf forwarding CONVERGENTE
 ip address {ip_lo200} 255.255.255.255
!
!
router ospf 200 vrf CONVERGENTE
 router-id {ospf_rid}
 redistribute bgp 65000
 passive-interface Loopback200
 default-information originate always
!
router bgp 65000
 address-family ipv4 vrf CONVERGENTE
  network {ip_lo200} mask 255.255.255.255
  redistribute connected
  redistribute static
  redistribute ospf 200 match internal external 1 external 2
 exit-address-family
'''

print()
print("-" *70)
print(f"Configuração Convergente - RAGG{sites_id[site_id]}:".center(70))
print("-" *70)
print()
print(output)
print()