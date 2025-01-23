from kafka import KafkaConsumer

def consumir_mensagens(topico, bootstrap_servers, group_id):
    try:
        # Configura o consumidor do Kafka
        consumer = KafkaConsumer(
            topico,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            auto_offset_reset='earliest',  # Começa desde o início se não houver commits
            enable_auto_commit=True,       # Faz commit automático dos offsets
            value_deserializer=lambda x: x.decode('utf-8')  # Decodifica as mensagens como texto
        )

        print(f"Consumindo mensagens do tópico: {topico}")
        for mensagem in consumer:
            print(f"Mensagem recebida: {mensagem.value}")
    
    except Exception as e:
        print(f"Erro ao consumir mensagens: {e}")
    finally:
        if 'consumer' in locals():
            consumer.close()

if __name__ == "__main__":
    # Configurações
    TOPICO = "topic.db_eng_dados.acoes"
    BOOTSTRAP_SERVERS = ["localhost:9092"]  # Use "kafka:9093" se estiver dentro do container
    GROUP_ID = "1"      # Altere conforme necessário

    consumir_mensagens(TOPICO, BOOTSTRAP_SERVERS, GROUP_ID)