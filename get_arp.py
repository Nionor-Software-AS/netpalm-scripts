# Nionor Software AS
# Custom scripts for https://github.com/tbotnz/netpalm
# Get Cisco arp, with VRF and interface support.
from netmiko import ConnectHandler
import logging


log = logging.getLogger(__name__)



def run(**kwargs):
    try:
        args = kwargs.get("kwargs")
        device = {
            'device_type': 'cisco_ios',
            'ip': args['hostname'],
            'username': args['username'],
            'password': args['password']
        }
        net_connect = ConnectHandler(**device)

        if args['from_all_vrfs']:
            vrf_arp_entries = {}
            arp = net_connect.send_command('show ip arp', use_textfsm=True)
            vrfs = net_connect.send_command('show vrf', use_textfsm=True)
            for vrf in vrfs:
                command = f"show ip arp vrf {vrf['name']}"
                output = net_connect.send_command(command, use_textfsm=True)
                vrf_arp_entries[vrf['name']] = output
            return {
                "arpa": arp,
                "vrf_arpa": vrf_arp_entries
            }
        else:
            if args['vrf_name'] and args['interface']:
                command = f"show arp vrf { args['vrf_name'] } interface { args['interface'] }"
            elif args['vrf_name']:
                command = f"show arp vrf { args['vrf_name'] }"
            elif args['interface']:
                command = f"show arp interface { args['interface'] }"
            else:
                command = "show arp"
            arp = net_connect.send_command(command, use_textfsm=True)
            return {
                "arpa": arp
            }

    except Exception as e:
        raise Exception(e)


