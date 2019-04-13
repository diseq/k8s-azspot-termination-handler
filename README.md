# K8s Azure Low-priority Preemption Termination Handler

This work is based on K8s Spot AWS Termination Handler for draining spot instances on AWS EC2.

## Table of contents
* [Introduction](#introduction)
* [Usage](#usage)
* [Related](#related)
* [Communication](#communication)
* [Contributing](#contributing)
* [License](#license)

## Introduction

The K8s Azure Spot Termination handler watches the Azure scheduled events service when running on Low-priority Instances.

When a Low Priority Instance is due to be terminated, precisely 30 secons before it's
termination a "termination notice" is issued.
The K8s Azure Spot Termination Handler watches for this and then gracefully drains the
node it is running on before the node is taken away by AWS.

## Usage

### Deploy to Kubernetes
A docker image is available at `docker.io/diseq/k8s-azspot-termination-handler`.
These images are currently built on pushes to master. Releases will be tagged as and when releases are made.

Sample Kubernetes manifests are available in the [deploy](deploy/) folder.

To deploy in clusters using RBAC, please apply all of the manifests (Daemonset, ClusterRole, ClusterRoleBinding and ServiceAccount) in the [deploy](deploy/) folder but uncomment the `serviceAccountName` in the [Daemonset](deploy/daemonset.yaml).

#### Requirements

For the K8s Termination Handler to schedule correctly; you will need an identifying label on your low-priority instances.

We add a label `node-role.kubernetes.io/azspot-worker` to our low-priority instances and hence this is the default value in the node selector of the [Daemonset](deploy/daemonset.yaml).
```yaml
nodeSelector:
  "node-role.kubernetes.io/azspot-worker": "true"
```
To achieve this, add the following flag to your Kubelet:
```
--node-labels="node-role.kubernetes.io/azspot-worker=true"
```

## Related
- [K8s Spot AWS Termination Handler](https://github.com/pusher/k8s-spot-termination-handler): K8s AWS Spot Preemption Termination Handler
- [K8s Spot Rescheduler](https://github.com/pusher/k8s-spot-rescheduler): Move nodes from on-demand instances to spot instances when space is available.

## Communication

* Found a bug? Please open an issue.
* Have a feature request. Please open an issue.
* If you want to contribute, please submit a pull request

## Contributing
Please see our [Contributing](CONTRIBUTING.md) guidelines.

## License
This project is licensed under Apache 2.0 and a copy of the license is available [here](LICENSE).
