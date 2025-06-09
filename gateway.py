# gateway.py
from confluent_kafka import Consumer, Producer, KafkaException
import json
import Ice

Ice.loadSlice('Calculator.ice')
import Demo


class KafkaCalculatorGateway:
    def __init__(self, kafka_config, request_topic, response_topic, ice_proxy):
        self.consumer = Consumer(kafka_config)
        self.producer = Producer(kafka_config)
        self.request_topic = request_topic
        self.response_topic = response_topic
        self.ice_proxy = ice_proxy

        # Configuración de Ice
        self.calculator = Demo.CalculatorPrx.checkedCast(
            Ice.initialize().stringToProxy(ice_proxy)
        )

    def process_request(self, msg):
        try:
            data = json.loads(msg.value().decode('utf-8'))
            req_id = data.get('id')
            operation = data.get('operation')
            operands = data.get('args', {})

            # Validación básica del formato
            if not req_id or not operation or not operands:
                raise ValueError("Campos requeridos faltantes")

            op1 = operands.get('op1')
            op2 = operands.get('op2')

            if op1 is None or op2 is None:
                raise ValueError("Operandos incompletos")

            # Ejecutar operación en Ice
            if operation == "sum":
                result = self.calculator.sum(op1, op2)
            elif operation == "sub":
                result = self.calculator.sub(op1, op2)
            elif operation == "mult":
                result = self.calculator.mult(op1, op2)
            elif operation == "div":
                result = self.calculator.div(op1, op2)
            else:
                raise ValueError(f"Operación no soportada: {operation}")

            # Enviar respuesta exitosa
            response = {
                "id": req_id,
                "status": True,
                "result": result
            }

        except Exception as e:
            # Manejo de errores genéricos
            response = {
                "id": req_id or "unknown",
                "status": False,
                "error": str(e)
            }

        self.producer.produce(
            self.response_topic,
            json.dumps(response).encode('utf-8')
        )
        self.producer.flush()

    def run(self):
        self.consumer.subscribe([self.request_topic])
        print("Gateway running...")
        try:
            while True:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None: continue
                if msg.error():
                    raise KafkaException(msg.error())
                self.process_request(msg)
        except KeyboardInterrupt:
            pass
        finally:
            self.consumer.close()
            self.communicator.destroy()


if __name__ == "__main__":
    config = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'calculator-group',
        'auto.offset.reset': 'earliest'
    }

    gateway = KafkaCalculatorGateway(
        kafka_config=config,
        request_topic="calculator_requests",
        response_topic="calculator_responses",
        ice_proxy="calculator:default -p 10000"
    )
    gateway.run()