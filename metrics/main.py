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
    `READ`: a comma separated list of sensor typ, sensor number, with the attribute to read. Example:
    `READ=R6.status,R8.status,A1.as_tc4012,A2.value,C2.value`
    """
    relays = ipx.relays
    analogs = ipx.analogs
    data = f"""# TYPE gce_ipx800_relays gauge
gce_ipx800_relays{{host="{ipx_host}", relay="R1"}} {1 if relays[0].status else 0}
gce_ipx800_relays{{host="{ipx_host}", relay="R6"}} {1 if relays[5].status else 0}
# TYPE gce_ipx800_analogs gauge
gce_ipx800_analogs{{host="{ipx_host}", analog="A1"}} {round(analogs[0].as_tc100, 3)}
gce_ipx800_analogs{{host="{ipx_host}", analog="A2"}} {round(analogs[1].as_tc100, 3)}
"""
    return Response(content=data, media_type="text/plain")
