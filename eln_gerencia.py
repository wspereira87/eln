from rich import print
import ipaddress
import json

print()
print("#" * 70)
print("Gerador de scripts para REDE DE GERÊNCIA - Eletronorte".center(70))
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
ce_hostname = str.upper(input(f"Informe o hostname do CE: "))
print()
pe_intf = str.upper(input(f"Informe a interface do Agregador (GIX/X/X): "))
print()
ce_intf = str.upper(input(f"Informe a interface do CE (GIX/X/X): "))
print()
p2p_net = str(input(f"Informe a rede P2P de gerência (172.27.250.X/28): "))
print()

# Verificar forma de extrair a máscara para colocar na BDI.
ip_p2p_pe = list(ipaddress.ip_network(p2p_net).hosts())[-2]
ip_p2p_ce = list(ipaddress.ip_network(p2p_net).hosts())[-1]
ip_oob_pe = list(ipaddress.ip_network(p2p_net).hosts())[0]

output = f'''interface {pe_intf}
 description TRUNK - {ce_hostname}-{ce_intf} - GERENCIA
 mtu 9202
 no ip address
 negotiation auto
 load-interval 30
 service instance trunk 2 ethernet
  description == L2 CONTROL PROTOCOL PEERING (CDP,STP) AND L2 SWTICHING ==
  encapsulation dot1q 250
  rewrite ingress tag pop 1 symmetric
  l2protocol peer cdp stp
  bridge-domain from-encapsulation
  service-policy input FROM_MGMT
!
interface BDI250
 description Gerencia
 ip vrf forwarding GERENCIA
 ip address {ip_p2p_pe} 255.255.255.240
 shutdown
!
!
router bgp 65000
 address-family ipv4 vrf GERENCIA
  redistribute connected
  redistribute static
 exit-address-family
 !
!
ip route vrf Mgmt-intf 0.0.0.0 0.0.0.0 {ip_p2p_ce}
!
!
interface GigabitEthernet0
 description Gerencia OOB
 vrf forwarding Mgmt-intf
 ip address {ip_oob_pe} 255.255.255.240
 negotiation auto
'''

print()
print("-" *70)
print(f"Configuração de Gerência - RAGG{sites_id[site_id]}:".center(70))
print("-" *70)
print()
print(output)
print()