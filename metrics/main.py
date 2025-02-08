import os

from fastapi import FastAPI, Response

from ipx800 import ipx800

app = FastAPI()
ipx_host = os.getenv("IPX_API_URL")
ipx = ipx800(ipx_host, os.getenv("IPX_API_KEY"))


@app.get("/metrics")
def gce_ipx800_metrics():
    """
    Return metrics for the GCE IPX800 device based on the entries to read from the environment
    variable `READ`.
    `READ`: a comma separated list of sensor type, sensor number, with the attribute to read. Example:
    `READ=R6,R1,A1.as_tc4012,A2.value,C1`
    If READ is not provided it will return all values.
    """
    relays = []
    analogs = []
    counters = []
    all = False
    for value in os.getenv("READ", "").split(","):
        if value.startswith("A"):
            analogs.append(value.split("."))
        elif value.startswith("R"):
            relays.append(value)
        elif value.startswith("C"):
            counters.append(value)
    else:
        all = True

    data = ""
    if analogs or all:
        data += "# TYPE gce_ipx800_analogs gauge\n"
        data += "# HELP gce_ipx800_analogs Value of the analog sensors\n"
        for a in analogs:
            idx = int(a[0][1:])
            attribute = a[1]
            data += f'gce_ipx800_analogs{{host="{ipx_host}", analog="{a[0]}"}} {round(getattr(ipx.analogs[idx - 1], attribute), 3)}\n'
        else:
            for index, val in enumerate(ipx.analogs):
                data += f'gce_ipx800_analogs{{host="{ipx_host}", analog="A{index + 1}"}} {round(val.value, 3)}\n'

    if counters or all:
        data += "# TYPE gce_ipx800_counters_total counter\n"
        data += "# HELP gce_ipx800_counters_total Value of the counters\n"
        for c in counters:
            idx = int(c[1:])
            data += f'gce_ipx800_counters_total{{host="{ipx_host}", counter="{c}"}} {ipx.counters[idx - 1].value}\n'
        else:
            for index, val in enumerate(ipx.counters):
                data += f'gce_ipx800_counters_total{{host="{ipx_host}", counter="C{index + 1}"}} {val.value}\n'

    if relays or all:
        data += "# TYPE gce_ipx800_relays_state gauge\n"
        data += (
            "# HELP gce_ipx800_relays_state Status of the relay, either 0=OFF or 1=ON\n"
        )
        for r in relays:
            idx = int(r[1:])
            data += f'gce_ipx800_relays_state{{host="{ipx_host}", relay="{r}"}} {int(ipx.relays[idx - 1].status)}\n'
        else:
            for index, val in enumerate(ipx.relays):
                data += f'gce_ipx800_relays_state{{host="{ipx_host}", relay="R{index + 1}"}} {int(val.status)}\n'

    data += "# EOF\n"

    return Response(content=data, media_type="text/plain; version=0.0.4; charset=utf-8")
