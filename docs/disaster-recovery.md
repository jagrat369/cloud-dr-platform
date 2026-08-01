# Disaster Recovery Plan

This document will contain the tested disaster recovery procedure.

## Recovery objectives

Do not enter target RTO/RPO numbers until they have been measured.

- Target RTO: TBD
- Target RPO: TBD

## Failure scenarios

### 1. Application container failure

Kubernetes should restart or replace an unhealthy pod.

### 2. Application health failure

The load balancer should stop sending traffic to an unhealthy application instance.

### 3. Primary-region failure

The DR environment should become the traffic destination after the failover conditions are met.

### 4. Database recovery

The DR environment must use the documented database backup/replication strategy.

## Test evidence

For every failure test, record:

- Failure start time
- Detection time
- Failover start time
- Application recovery time
- Data recovery point
- Total recovery time
- Observed errors

Actual measurements belong here after testing.
