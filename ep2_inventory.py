from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get


'''
nr = InitNornir(
    config_file="nornir.yaml", dry_run=True
)

nr = InitNornir(
    config_file="config.yaml",
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 50,
        },
    },
)
'''
nr = InitNornir(
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 100,
        },
    },
    inventory={
        "plugin": "SimpleInventory",
        "options": {
            "host_file": "inventory/hosts.yaml",
            "group_file": "inventory/groups.yaml"
        },
    },
)


print(nr.inventory.hosts)
print(nr.inventory.groups)
R1 = nr.inventory.hosts["R1"]
print(R1.keys())
print(R1['bgp_source'])
print(R1['name_servers'])
results = nr.run(
    task=napalm_get, getters=["facts", "interfaces"]
)
print_result(results)