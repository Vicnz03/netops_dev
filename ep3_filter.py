from nornir import InitNornir
from nornir_utils.plugins.functions import print_result
from nornir_napalm.plugins.tasks import napalm_get


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

target = nr.filter(hostname="R1").inventory.hosts.keys()
target = nr.filter(prefix="CE").inventory.hosts.keys()

#You can also filter using multiple <key, value> pairs:
target = nr.filter(hostname="R1", prefix="CE").inventory.hosts.keys()




def has_long_name(host):
    return len(host.name) == 11

nr.filter(filter_func=has_long_name).inventory.hosts.keys()
nr.filter(filter_func=lambda h: len(h.name) == 9).inventory.hosts.keys()

from nornir.core.filter import F
linux_or_eos = nr.filter(F(platform="linux") | F(platform="eos"))
cmh_and_spine = nr.filter(F(groups__contains="cmh") & F(role="spine"))
cmh_and_not_spine = nr.filter(F(groups__contains="cmh") & ~F(role="spine"))
nested_string_asd = nr.filter(F(nested_data__a_string__contains="asd"))
results = nr.run(
    task=napalm_get, getters=["facts", "interfaces"]
)
print_result(results)