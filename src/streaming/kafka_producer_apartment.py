import argparse
import json
import time
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from kafka import KafkaProducer
from config import paths

def safe_row_dict(row):
    data = {}
    for k, v in row.items():
        if pd.isna(v): data[k] = None
        elif isinstance(v, pd.Timestamp): data[k] = v.isoformat()
        elif isinstance(v, np.generic): data[k] = v.item()
        else: data[k] = v
    return data

def main():
    parser = argparse.ArgumentParser(description="Envia imóveis para o Kafka.")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--topic", type=str, default="real_estate_listings")
    parser.add_argument("--bootstrap-servers", type=str, default="localhost:9092")
    args = parser.parse_args()

    # Inicializa o Producer
    producer = KafkaProducer(
        bootstrap_servers=args.bootstrap_servers,
        value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8')
    )

    kafka_path = paths.CURATED / "apartment_kafka_holdout.parquet"
    df = pd.read_parquet(kafka_path).reset_index(drop=True)
    total = len(df)
    idx = 0

    print(f"A enviar para o tópico '{args.topic}'... (Ctrl+C para parar)")
    
    try:
        while True:
            row = df.iloc[idx % total]
            idx += 1
            
            msg = {
                "event_id": f"evt_{idx}",
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "listing": safe_row_dict(row),
            }
            
            # Envia para o Kafka
            producer.send(args.topic, value=msg)
            print(f"✅ Enviado: {msg['event_id']}")
            
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n🛑 Producer parado.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()