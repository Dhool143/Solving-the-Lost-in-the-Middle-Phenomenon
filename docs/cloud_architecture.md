
# Cloud Architecture Guide

## Virtual Private Cloud (VPC)

A Virtual Private Cloud (VPC) is a logically isolated
network within AWS. It allows organizations to control
network settings, IP address ranges, subnets, and routing.

## Public and Private Subnets

Public subnets can provide routes to an internet gateway.

Private subnets do not have a direct route to an internet
gateway. Applications and databases can be placed in
private subnets to reduce direct internet exposure.

## AWS Lambda

AWS Lambda is a serverless computing service that
runs code without requiring users to manage servers.

Lambda can process events, execute backend logic,
and connect to other AWS services.

## Kubernetes

Kubernetes is a container orchestration platform.
It helps deploy, scale, and manage containerized
applications.

Worker nodes run application workloads in pods.
Their resource requirements depend on the workloads,
container runtime, and Kubernetes configuration.
