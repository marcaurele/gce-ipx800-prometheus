# GCE IPX800 metrics exporter

This project contains a container image available at `` to expose the sensor values in Prometheus format.

## Configuration

It an expose all IPX800 values, or it can only return a subset of them by defining the environment varialbe `READ` as a comma separated list of sensor type and index value, with the attribute to read. An example would be:

```
READ=R6.status,R8.status,A1.as_tc4012,A2.value,C2.value
```