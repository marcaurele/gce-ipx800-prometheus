# GCE IPX800 metrics exporter

***WORK IN PROGRESS***

This project contains a container image available at `` to expose the sensor values in Prometheus format for the GCE IPX800 device in order to graph those on Grafana.

Currently it can expose:

* Analog sensors
* Counters
* Relay statuses

## Configuration

It an expose all IPX800 values, or it can only return a subset of them by defining the environment variable `READ` as a comma separated list of sensor type and index value, with the attribute to read. An example would be:

```console
docker run --rm \
    -e IPX_API_URL=http://<ipx800> \
    -e IPX_API_KEY=<apikey> \
    -e READ=R6,R8,A1.as_tc100,A2.as_tc100,C1 \
    -p 8333:8333 ipx800-prom
```
