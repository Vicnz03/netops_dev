from nornir import InitNornir
from nornir_jinja2.plugins.tasks import template_file
from nornir.core.exceptions import NornirSubTaskError
import csv
import ipaddress
import getpass
import logging
import sys
from time import sleep

logger = logging.getLogger(__name__)


def generate_config(task, dmz):
    result = task.run(task=template_file, name="Generate configuration",
                      template=f"{task.host.groups[0]}.j2", path='templates/HF_dmz', dmz=dmz, counter=task.host['counter'], site=task.host['site']).result

    task.host['config'] = result.split('\n')

    with open(f'HF_dmz/config/{task.host.name}.conf', 'w') as f:
        f.write(result)


if __name__ == '__main__':
    username = getpass.getuser()
    password = getpass.getpass()

    # Init Nornir
    nr = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": "inventory/HF_hosts.yaml",
                "group_file": "inventory/groups.yaml"
            }
        }
    )
    nr.inventory.defaults.username = username
    nr.inventory.defaults.password = password

    with open('HF_dmz/DMZ.csv', 'r', encoding='utf-8-sig') as f:
        dmz = list(csv.DictReader(f))

    rt_query = "SELECT route_target FROM config_routing_instances WHERE routing_instances_name = '{}';"
    for zone in dmz:
        zone['vrf_rt'] = nagios_query(rt_query.format(zone['vrf']))[0][0]
        zone['net_addr'] = ipaddress.ip_address(zone['ipv4'].split('/')[0])

        for site in ['AKL1', 'AKL2', 'CHC1', 'CHC2']:
            zone[f'vpls_{site}'] = f'CUSTOMER_VPLS_PegasusHealth_HF_{zone["vpls_prefix"]}_{site}'
            try:
                zone[f'vpls_rt_{site}'] = nagios_query(
                    rt_query.format(zone[f'vpls_{site}']))[0][0]
            except:
                print(zone[f'vpls_{site}'] + ':error , please check')

    nr.run(task=generate_config, dmz=dmz)
    juniper= nr.filter(filter_func=lambda h: h.platform != 'fortinet')
    juniper.run(task=junos_config, mode='compare',commands = ['already_there'])
