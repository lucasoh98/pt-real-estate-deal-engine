import argparse
from config import paths
import json
import numpy as np
import pandas as pd
import joblib
from kafka import KafkaConsumer

def load_models():
    model_dir = paths.MODELS
    if not model_dir.exists():
        raise FileNotFoundError("Diretório de modelos não encontrado.")

    model_files = sorted(model_dir.glob("apartment_*.pkl"))
    if not model_files:
        raise FileNotFoundError("Nenhum modelo encontrado em /models (apartment_*.pkl).")

    models = []
    for path in model_files:
        payload = joblib.load(path)
        models.append({"name": path.stem, "payload": payload})
    return models

def prepare_features(payload, listing):
    features = payload.get("features")
    cat_cols = payload.get("cat_cols", [])
    model_type = payload.get("type", "lgbm")

    # Cria o DataFrame e garante que todas as colunas esperadas existem
    X = pd.DataFrame([listing])
    for f in features:
        if f not in X.columns:
            X[f] = 0
    
    X = X[features].copy()

    # Identifica colunas numéricas (as que não são categóricas)
    num_cols = [c for c in features if c not in cat_cols]
    
    # CONVERSÃO ROBUSTA: Transforma tudo o que deve ser número e limpa lixo
    for col in num_cols:
        X[col] = pd.to_numeric(X[col], errors='coerce').fillna(0)

    # Trata as colunas categóricas para o LightGBM
    if model_type == "lgbm":
        for c in cat_cols:
            if c in X.columns:
                X[c] = X[c].astype("category")
    return X

def main():
    parser = argparse.ArgumentParser(description="Consome imóveis do Kafka e avalia deals.")
    parser.add_argument("--min-discount", type=float, default=0.15)
    parser.add_argument("--topic", type=str, default="real_estate_listings")
    parser.add_argument("--bootstrap-servers", type=str, default="localhost:9092")
    args = parser.parse_args()

    # Carrega os modelos treinados
    try:
        models = load_models()
    except Exception as e:
        print(f"❌ Erro ao carregar modelos: {e}")
        return

    # Inicializa o Consumer do Kafka
    consumer = KafkaConsumer(
        args.topic,
        bootstrap_servers=args.bootstrap_servers,
        auto_offset_reset='earliest',
        group_id='deal-engine-group',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )

    print(f"🎯 A aguardar por mensagens em '{args.topic}'...")

    try:
        for message in consumer:
            msg = message.value
            listing = msg.get("listing", {})
            event_id = msg.get("event_id", "unknown")
            true_price = listing.get("Price")

            if true_price is None:
                continue

            print(f"\n🏠 Imóvel: {event_id} | Preço real: {float(true_price):,.0f} €")

            for item in models:
                payload = item["payload"]
                model = payload["model"]
                
                X = prepare_features(payload, listing)

                # Realiza a previsão (o modelo espera Log Price, por isso usamos expm1 depois)
                pred_log = model.predict(X)[0]
                pred = float(np.expm1(pred_log))
                
                # Calculado o desconto (Preço Estimado vs Preço Real)
                discount = 1 - (float(true_price) / pred)
                
                # Define se é um bom negócio ou mau negócio 
                status = "✅" if discount >= args.min_discount else "❌"
                print(f"   {status} {item['name']} | previsto: {pred:,.0f} € | desc: {discount:+.1%}")

    except KeyboardInterrupt:
        print("\n🛑 Consumer parado pelo utilizador.")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    main()