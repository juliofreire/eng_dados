from kafka import KafkaConsumer

# Criar o consumidor
consumer = KafkaConsumer('test', bootstrap_servers='localhost:9092')

# Consumir mensagens
for message in consumer:
        print(f"Mensagem recebida: {message.value.decode('utf-8')}")
