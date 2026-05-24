"""
Iris Flower Classification
--------------------------
Trains and evaluates three ML models on the classic Iris dataset.
Models: Logistic Regression, Decision Tree, K-Nearest Neighbors
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report,
    confusion_matrix, ConfusionMatrixDisplay
)

# ── Config ────────────────────────────────────────────────────────────────────
DATA_PATH   = os.path.join(os.path.dirname(__file__), '..', 'data', 'iris.csv')
OUTPUT_DIR  = os.path.join(os.path.dirname(__file__), '..', 'outputs')
RANDOM_SEED = 42
TEST_SIZE   = 0.20
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    print(f"[data] Loaded {df.shape[0]} rows × {df.shape[1]} columns")
    print(f"[data] Class distribution:\n{df['species'].value_counts()}\n")
    return df


# ── Preprocessing ─────────────────────────────────────────────────────────────
def preprocess(df: pd.DataFrame):
    feature_cols = [c for c in df.columns if c != 'species']
    X = df[feature_cols].values
    y = df['species'].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_SEED, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test  = scaler.transform(X_test)

    print(f"[split] Train: {X_train.shape[0]} | Test: {X_test.shape[0]}\n")
    return X_train, X_test, y_train, y_test, scaler


# ── Models ────────────────────────────────────────────────────────────────────
def get_models() -> dict:
    return {
        'Logistic Regression': LogisticRegression(max_iter=200, random_state=RANDOM_SEED),
        'Decision Tree':       DecisionTreeClassifier(max_depth=4, random_state=RANDOM_SEED),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    }


# ── Train & Evaluate ──────────────────────────────────────────────────────────
def train_and_evaluate(models, X_train, X_test, y_train, y_test) -> dict:
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)

        acc = accuracy_score(y_test, preds)
        cv  = cross_val_score(model, X_train, y_train, cv=5).mean()
        results[name] = {'model': model, 'accuracy': acc, 'cv_accuracy': cv, 'preds': preds}

        print(f"── {name} ──")
        print(f"   Test Accuracy : {acc:.4f}")
        print(f"   CV  Accuracy  : {cv:.4f}")
        print(classification_report(y_test, preds, zero_division=0))

    return results


# ── Plots ─────────────────────────────────────────────────────────────────────
def plot_model_comparison(results: dict):
    names = list(results.keys())
    accs  = [results[n]['accuracy'] * 100 for n in names]
    cvs   = [results[n]['cv_accuracy'] * 100 for n in names]

    x = np.arange(len(names))
    width = 0.35
    colors = ['#FF6B6B', '#4ECDC4']

    fig, ax = plt.subplots(figsize=(9, 5))
    b1 = ax.bar(x - width/2, accs, width, label='Test Accuracy',  color=colors[0], alpha=0.9)
    b2 = ax.bar(x + width/2, cvs,  width, label='CV Accuracy',    color=colors[1], alpha=0.9)

    ax.set_xticks(x); ax.set_xticklabels(names, fontsize=11)
    ax.set_ylabel('Accuracy (%)', fontsize=12)
    ax.set_title('Model Comparison — Test vs Cross-Validation Accuracy', fontsize=13, fontweight='bold')
    ax.set_ylim(80, 105)
    ax.legend(); ax.grid(axis='y', alpha=0.3)

    for bar in list(b1) + list(b2):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
                f'{bar.get_height():.1f}%', ha='center', va='bottom', fontsize=9, fontweight='bold')

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'model_comparison.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[plot] Saved {out}")


def plot_confusion_matrix(results: dict, y_test):
    best = max(results, key=lambda n: results[n]['accuracy'])
    cm   = confusion_matrix(y_test, results[best]['preds'])

    fig, ax = plt.subplots(figsize=(7, 6))
    disp = ConfusionMatrixDisplay(cm, display_labels=['setosa', 'versicolor', 'virginica'])
    disp.plot(ax=ax, colorbar=True, cmap='Blues')
    ax.set_title(f'Confusion Matrix — {best}', fontsize=13, fontweight='bold')
    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'confusion_matrix.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[plot] Saved {out}")


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    df = load_data(DATA_PATH)
    X_train, X_test, y_train, y_test, scaler = preprocess(df)
    models  = get_models()
    results = train_and_evaluate(models, X_train, X_test, y_train, y_test)
    plot_model_comparison(results)
    plot_confusion_matrix(results, y_test)

    best = max(results, key=lambda n: results[n]['accuracy'])
    print(f"\n🏆 Best Model : {best}  ({results[best]['accuracy']*100:.1f}% test accuracy)")
