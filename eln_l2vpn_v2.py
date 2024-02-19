from rich import print
import json

print()
print("#" * 70)
print("Gerador de scripts para L2VPN - Eletronorte".center(70))
print("#" * 70)
print()

conn_text = '''Conexão do cliente: (1 ou 2)
1 - Agregador
2 - Switch\n\n'''

conn = str(input(conn_text))
print()
if conn not in ("1", "2"):
    print("OPÇÃO INVÁLIDA!\n")
else:
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
       17: "TPJ"
    }
        
    client_name = str.upper(input(f"Informe o nome do cliente: "))
    print()
    site1 = int(input(f"Informe o ID do Site 1: \n\n{json.dumps(sites_id, indent=4)}\n\n"))
    print()
    site2 = int(input(f"Informe o ID do Site 2: \n\n{json.dumps(sites_id, indent=4)}\n\n"))
    print()
    client_id = int(input("Informe a VLAN/ID do cliente: "))
    print()
    
    if conn == "1":
        client_intf1 = str.upper(input(f"Informe a interface do agregador de {sites_id[site1]} (TEX/X/X): "))
        print()
        client_intf2 = str.upper(input(f"Informe a interface do agregador {sites_id[site2]} (TEX/X/X): "))
        print()
        output1 = f'''interface {client_intf1}
 description L2VPN - {client_name} - {sites_id[site1]}_{sites_id[site2]}
 service instance {client_id} ethernet
  description L2VPN - {client_name} - {sites_id[site1]}_{sites_id[site2]}
  encapsulation dot1q {client_id} [default | untagged]
  rewrite ingress tag pop 1 symmetric
  service-policy input FROM_SCM
  l2protocol tunnel dot1x elmi esmc lacp lldp loam mmrp cdp mvrp pagp ptppd stp udld vtp [opcional]
 !
!
interface Pseudowire {client_id}
 description {client_name} - {sites_id[site1]}_{sites_id[site2]}
 encapsulation mpls
 control-word include
 load-balance flow ethernet src-dst-mac
 load-balance flow-label both
 neighbor 172.27.254.{site2} {client_id}
!
l2vpn xconnect context {client_name}
  member {client_intf1} service-instance {client_id}
  member Pseudowire {client_id}
!
'''
        output2 = f'''interface {client_intf2}
 description L2VPN - {client_name} - {sites_id[site2]}_{sites_id[site1]}
 service instance {client_id} ethernet
  description L2VPN - {client_name} - {sites_id[site2]}_{sites_id[site1]}
  encapsulation default [dot1q {client_id} | untagged]
  service-policy input FROM_SCM
  l2protocol tunnel dot1x elmi esmc lacp lldp loam mmrp cdp mvrp pagp ptppd stp udld vtp [opcional]
 !
!
interface Pseudowire {client_id}
 description {client_name} - {sites_id[site2]}_{sites_id[site1]}
 encapsulation mpls
 control-word include
 load-balance flow ethernet src-dst-mac
 load-balance flow-label both
 neighbor 172.27.254.{site1} {client_id}
!
l2vpn xconnect context {client_name}
  member {client_intf2} service-instance {client_id}
  member Pseudowire {client_id}
!
'''
    elif conn == "2":
        intf_sw = "PO40"
        output1 = f'''interface {intf_sw}
 service instance {client_id} ethernet
  description L2VPN - {client_name} - {sites_id[site1]}_{sites_id[site2]}
  encapsulation dot1q {client_id} [default | untagged]
  rewrite ingress tag pop 1 symmetric
  service-policy input FROM_SCM
  l2protocol tunnel dot1x elmi esmc lacp lldp loam mmrp cdp mvrp pagp ptppd stp udld vtp [opcional]
 !
!
interface Pseudowire {client_id}
 description {client_name} - {sites_id[site1]}_{sites_id[site2]}
 encapsulation mpls
 control-word include
 load-balance flow ethernet src-dst-mac
 load-balance flow-label both
 neighbor 172.27.254.{site2} {client_id}
!
l2vpn xconnect context {client_name}
  member {intf_sw} service-instance {client_id}
  member Pseudowire {client_id}
!
'''
        output2 = f'''interface {intf_sw}
 service instance {client_id} ethernet
  description L2VPN - {client_name} - {sites_id[site2]}_{sites_id[site1]}
  encapsulation dot1q {client_id} [default | untagged]
  rewrite ingress tag pop 1 symmetric
  l2protocol tunnel dot1x elmi esmc lacp lldp loam mmrp cdp mvrp pagp ptppd stp udld vtp [opcional]
 !
!
interface Pseudowire {client_id}
 description {client_name} - {sites_id[site2]}_{sites_id[site1]}
 encapsulation mpls
 control-word include
 load-balance flow ethernet src-dst-mac
 load-balance flow-label both
 neighbor 172.27.254.{site1} {client_id}
!
l2vpn xconnect context {client_name}
  member {intf_sw} service-instance {client_id}
  member Pseudowire {client_id}
!
'''
    else:
        print("OPÇÃO INVÁLIDA!")
    
    
    print("-" *70)
    print(f"Configuração RAGG{sites_id[site1]}:".center(70))
    print("-" *70)
    print(output1)
    print()
    print("-" *70)
    print(f"Configuração RAGG{sites_id[site2]}:".center(70))
    print("-" *70)
    print(output2)
    print()