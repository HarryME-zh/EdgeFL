# EdgeFL Framework

The EdgeFL Framework simplifies the integration of decentralized federated learning into your machine learning applications. This framework allows peers to communicate, aggregate models, and participate in decentralized federated learning scenarios. The EdgeFL Python Framework offers functionalities like communication between peers for model aggregation, serving model files using Flask, registering and unregistering with the registration node, and customizable aggregation functions. By using this framework, you can easily enable collaborative training across distributed devices.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Configuration](#configuration)
- [Peer Registration and Lookup](#peer-registration-and-lookup)
- [Example Usage: Training a Federated Learning Model](#example-usage-training-a-federated-learning-model)
- [Docker Configuration for Peer and Registration Node](#docker-configuration-for-peer-and-registration-node)
- [Deployment with Docker Swarm](#deployment-with-docker-swarm)
- [License](#license)

## Introduction

The EdgeFL Python Framework enables machine learning developers to easily integrate decentralized federated learning functionality into their applications. It allows peers to communicate, aggregate models, and participate in decentralized training scenarios. This framework empowers collaborative training across distributed devices, making it a powerful tool for edge computing environments.

## Installation

To install the EdgeFL Python Framework, follow these steps:

1. Clone the repository to your local machine:

    ```
   bash
   git clone https://github.com/your-username/EdgeFL.git
   cd EdgeFL
   ```

2. Install the required dependencies using pip:
      ```
   pip install -r requirements.txt
   ```
 

## Getting Started

To get started with the EdgeFL Python Framework, follow the example below to integrate the decentralized federated learning functionality into your application:

1.  Import the necessary modules and create a `Peer` instance:
    
    ```
    from edgefl.peer import Peer
    
    REGISTRATION_ADDRESS = "registration-node-address"
    LOCAL_PORT = 5000
    FUNC_CONFIG = "functional_config.py"
    
    peer = Peer(REGISTRATION_ADDRESS, LOCAL_PORT, FUNC_CONFIG)
    ```
2.  Start the peer's functionality:
    
    `peer.start()` 
    
3.  Utilize your custom aggregation function using the provided functionalities.
    `w_latest = peer.aggregation_func()`

4. Unregister from the existing system after training.
    `peer.unregister_peer()`
    

## Configuration

The `functional_config.py` file contains the custom aggregation function used by the EdgeFL framework for federated learning. You can customize this function to suit your specific needs.

```
# Example functional_config.py
def FedAvg(models):
    # Your custom federated aggregation logic
    return aggregated_model
```
## Peer Registration and Lookup

The framework includes a `Registration` class that handles peer registration and lookup. Peers can register themselves with the registration node and perform peer lookups to discover each other for decentralized communication.

### Registration Process

1.  **Registering a Peer**:
    
    When a peer is started, it registers itself with the central registration node using an HTTP POST request. The peer's hostname, IP address, and port are recorded for later reference. The central registration node maintains a list of active peers.

    ```
    POST /register
    {
        "hostname": "peer-hostname"
    }
    ``` 
    
2.  **Unregistering a Peer**:
    
    When a peer is shut down, it sends an HTTP POST request to unregister itself from the central registration node. The central node removes the peer from the list of active peers.
    
    ```
    POST /unregister
    {
        "hostname": "peer-hostname"
    }
    ```
    

3. **Peer Lookup**:

-   To retrieve a list of active peers, peers can send an HTTP GET request to the central registration node:
    
    `GET /peers` 
    
-   The registration node responds with a JSON object containing a list of active peers' information.
    

## Example Usage: Training a Federated Learning Model

The provided `example.py` script demonstrates how to integrate the EdgeFL framework into your machine learning application. It uses the MNIST dataset to train a federated learning model, showcasing the integration of peer communication, model aggregation, and training functions.

## Docker Configuration for Peer and Registration Node

Containerize and deploy your EdgeFL framework components using Docker. Dockerfiles for the peer and registration node are provided, along with instructions for building and running the containers.

### Building and Running Containers

To build and run the Docker containers, follow these steps:

1.  Open a terminal.
    
2.  Navigate to the directory containing the `Dockerfile.peer` or `Dockerfile.registration` file.
    
3.  Build the Docker image for the component using the following command:
    
    ```
	docker build -t edgefl-peer -f Dockerfile.peer .
    # or
    docker build -t edgefl-registration -f Dockerfile.registration .
	```
    
4.  Run the Docker container using the following command:

    ```
	docker run -p <HOST_PORT>:<CONTAINER_PORT> -d edgefl-peer
    # or
    docker run -p <HOST_PORT>:<CONTAINER_PORT> -d edgefl-registration
    ```
    
Replace `<HOST_PORT>` with the port number on your host machine that you want to use to access the container, and `<CONTAINER_PORT>` with the port number specified in the `EXPOSE` directive in the Dockerfile.

## Deployment with Docker Swarm

Utilize Docker Swarm to orchestrate and manage your EdgeFL framework components. Provided deployment YAML files show how to deploy the peer and registration node components using Docker Swarm.

1.  Set up a Docker Swarm cluster if you haven't already.
    
2.  Save the content of `deployment-peer.yml` and `deployment-registration.yml` to separate files, for example, `peer-deployment.yml` and `registration-deployment.yml`.
    
3.  Deploy the components using the following commands:
    
    ```
    docker stack deploy -c peer-deployment.yml edgefl-peer-stack
    docker stack deploy -c registration-deployment.yml edgefl-registration-stack
    ```

## License

This project is licensed under the [MIT License](https://github.com/git/git-scm.com/blob/main/MIT-LICENSE.txt).
