from rich import print
import json

print()
print("#" * 70)
print("Gerador de scripts para REDE DE NEGÓCIOS - Eletronorte".center(70))
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
#vlan_id = int(input(f"Informe a VLAN da Convergente: "))
#print()
ce_hostname = str.upper(input(f"Informe o hostname do CE: "))
print()
pe_intf1 = str.upper(input(f"Informe a interface 1 do PO40 do Agregador (TEX/X/X): "))
print()
pe_intf2 = str.upper(input(f"Informe a interface 2 do PO40 do Agregador (TEX/X/X): "))
print()
ce_intf1 = str.upper(input(f"Informe a interface 1 do PO40 do CE (TEX/X/X): "))
print()
ce_intf2 = str.upper(input(f"Informe a interface 2 do PO40 do CE (TEX/X/X): "))
print()
intf_sw = "PO40"
print()

output1 = f'''interface {pe_intf1}
 description NEGOCIOS-{ce_hostname}-{ce_intf1} PO40
 mtu 9202
 no ip address
 load-interval 30
 channel-group 40 mode active
!
interface {pe_intf2}
 description NEGOCIOS-{ce_hostname}-{ce_intf2} PO40
 mtu 9202
 no ip address
 load-interval 30
 channel-group 40 mode active
!
!
interface {intf_sw}
 description NEGOCIOS {ce_hostname}-PO40
 mtu 9202
 no ip address
 load-interval 30
 shutdown
  service instance 1 ethernet
  encapsulation untagged
  l2protocol peer lacp
  bridge-domain 1
 !
 service instance 800 ethernet
  encapsulation dot1q 800
  rewrite ingress tag pop 1 symmetric
  service-policy input FROM_SCM
 !
!
interface Pseudowire 800
 description PW_TESTE_NEGOCIOS - {sites_id[site_id]}_SED
 encapsulation mpls
 control-word include
 load-balance flow ethernet src-dst-mac
 load-balance flow-label both
 neighbor 172.27.254.5 800{site_id}
!
l2vpn
 logging pseudowire status
 logging vc-state
!
l2vpn xconnect context TESTE_NEGOCIOS
  member {intf_sw} service-instance 800
  member Pseudowire 800
!
'''

output2 = f'''
interface Pseudowire 800{site_id}
 description PW_TESTE_NEGOCIOS - SED_{sites_id[site_id]}
 encapsulation mpls
 control-word include
 load-balance flow ethernet src-dst-mac
 load-balance flow-label both
 neighbor 172.27.254.{site_id} 800{site_id}
!
!
!#PRIMEIRO REMOVER SERVICE-INSTANCE DO XCONNECT DA MIGRAÇÃO ANTERIOR:
!
l2vpn xconnect context <XCONN_CONTEXT>
 no member PO40 service-instance 800
!
l2vpn xconnect context TESTE_NEGOCIOS_{sites_id[site_id]}
  member PO40 service-instance 800
  member Pseudowire 800{site_id}
!
'''

print()
print("-" *70)
print(f"Configuração Rede de Negócios - RAGG{sites_id[site_id]}:".center(70))
print("-" *70)
print()
print(output1)
print()
print("-" *70)
print(f"Configuração Rede de Negócios - RAGGSED:".center(70))
print("-" *70)
print()
print(output2)
print()
