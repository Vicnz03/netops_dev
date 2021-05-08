'''
self introduce
work through
Init nornir
run an example
'''

from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get


nr = InitNornir(
    runner={
        "plugin": "threaded",
        "options": {
            "num_workers": 20,
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

results = nr.run(
    task=napalm_get, getters=["facts", "interfaces"]
)
print_result(results)