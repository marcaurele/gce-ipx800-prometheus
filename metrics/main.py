from fastapi import FastAPI, Response


app = FastAPI()


@app.get("/metrics")
def gce_ipx800_metrics():
    """
    Return metrics for the GCE IPX800 device based on the entries to read from the environment
    variable `READ`.
    `READ`: a comma separated list of sensor typ, sensor number, with the attribute to read. Example:
    `READ=R6.status,R8.status,A1.as_tc4012,A2.value,C2.value`
    """
    data = """# HELP gce_ipx800_relays A metric for the relays
# TYPE gce_ipx800_relays gauge
"""
    return Response(content=data, media_type="text/plain")
