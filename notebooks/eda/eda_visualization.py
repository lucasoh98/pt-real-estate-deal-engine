import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def quick_dist_box(df, features=None, bins=40, sample_n=20000, top_k=10):
    if features is None:
        features = df.columns.tolist()

    for col in features:
        if col not in df.columns:
            continue

        s = df[col]
        is_num = pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s)

        print("=" * 80)
        print(f"{col} | dtype={s.dtype} | missing={s.isna().mean()*100:.2f}% | unique={s.nunique(dropna=True)}")

        # -------------------
        # NUMÉRICA: hist + box
        # -------------------
        if is_num:
            data_full = s.dropna()
            if len(data_full) == 0:
                print("Sem dados.")
                continue

            # amostra para acelerar plots
            data = data_full.sample(min(sample_n, len(data_full)), random_state=42)

            # cap só para visualização (evita gráficos esmagados por outliers)
            lo, hi = data.quantile(0.01), data.quantile(0.99)
            data_cap = data.clip(lo, hi)

            fig, axes = plt.subplots(1, 2, figsize=(12, 4))

            axes[0].hist(data_cap, bins=bins)
            axes[0].set_title(f"{col} — distribuição")

            axes[1].boxplot(data_cap, vert=True, showfliers=False)
            axes[1].set_title(f"{col} — boxplot (sem outliers)")

            plt.tight_layout()
            plt.show()

        # -------------------
        # CATEGÓRICA: top 10 bar
        # -------------------
        else:
            vc = s.astype("string").value_counts(dropna=False).head(top_k)

            plt.figure(figsize=(10, 4))
            plt.bar(vc.index.astype(str), vc.values)
            plt.title(f"{col} — top {min(top_k, len(vc))} categorias")
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.show()
            
def nan_report_simple(df_subset):
    return pd.DataFrame({
        "quantidade_nan": df_subset.isna().sum(),
        "percentagem_nan": (df_subset.isna().sum() / len(df_subset) * 100).round(2)
    }).sort_values("percentagem_nan", ascending=False)