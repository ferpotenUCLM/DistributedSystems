# Distributed Calculator with Ice and Kafka

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
![Kafka](https://img.shields.io/badge/Apache_Kafka-2.8%2B-orange)
![Ice](https://img.shields.io/badge/ZeroC_Ice-3.7%2B-lightgrey)

This project implements a distributed calculator using **ZeroC Ice** for RPC and **Apache Kafka** for asynchronous message handling. The system allows clients to submit mathematical operations through Kafka, which are processed by an Ice server via a gateway, with results returned via Kafka.

## Key Features

- 🧮 Basic math operations: addition, subtraction, multiplication, division
- ⚡ Asynchronous communication through Kafka
- 🛡️ Error handling (including division by zero)
- 📦 Modular and extensible architecture
- 🚀 Easy deployment and configuration

## Quick Installation

1. Clone the repository:
```bash
git clone https://github.com/your-user/distributed-calculator.git
cd distributed-calculator
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure Kafka (create the necessary topics):
```bash
.\bin\windows\kafka-topics.bat --create --topic calculator_requests --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
.\bin\windows\kafka-topics.bat --create --topic calculator_responses --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
```

## Basic Usage

1. Start the Ice server:
```bash
python server.py
```

2. Start the Kafka-Ice gateway:
```bash
python gateway.py
```

3. Send an operation:
```bash
echo {"id":"req1","operation":"sum","args":{"op1":5.0,"op2":3.0}} | .\bin\windows\kafka-console-producer.bat --topic calculator_requests --bootstrap-server localhost:9092
```

4. View the results:
```bash
.\bin\windows\kafka-console-consumer.bat --topic calculator_responses --bootstrap-server localhost:9092 --from-beginning
```

## Request Format

```json
{
"id": "unique-identifier",
"operation": "sum|sub|mult|div",
"args": {
"op1": 5.0,
"op2": 3.0
}
}
```

## Supported Operations

| Operation | Name in JSON |
|---------------|----------------|
| Addition | `sum` |
| Subtraction | `sub` |
| Multiplication | `mult` |
| Division | `div` |

## Complete Documentation

For advanced configuration, troubleshooting, and implementation details, see the [Project Wiki](https://github.com/ferpotenUCLM/DistributedSystems/wiki).


## License

This project is licensed under the [MIT License](LICENSE).

---

## requirements.txt
```txt
confluent-kafka==2.3.0
zeroc-ice==3.7.10
```
