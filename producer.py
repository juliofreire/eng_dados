from kafka import KafkaProducer

# Criar o produtor
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Enviar uma mensagem
producer.send('test', b'Hello, Kafka!')

# Fechar o produtor
producer.close()
