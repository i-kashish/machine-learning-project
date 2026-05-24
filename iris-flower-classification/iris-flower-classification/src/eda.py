"""
Iris Dataset — Exploratory Data Analysis
-----------------------------------------
Generates distribution histograms and scatter plots.
Run this before train.py to understand the data first.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

DATA_PATH  = os.path.join(os.path.dirname(__file__), '..', 'data', 'iris.csv')
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'outputs')
os.makedirs(OUTPUT_DIR, exist_ok=True)

COLORS = {'setosa': '#FF6B6B', 'versicolor': '#4ECDC4', 'virginica': '#45B7D1'}


def load_data():
    df = pd.read_csv(DATA_PATH)
    print("[EDA] Dataset info:")
    print(df.describe().round(2), '\n')
    print("[EDA] Missing values:", df.isnull().sum().sum())
    return df


def plot_distributions(df: pd.DataFrame):
    feature_cols = [c for c in df.columns if c != 'species']
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle('Feature Distributions by Species', fontsize=15, fontweight='bold')

    for ax, feat in zip(axes.flat, feature_cols):
        for sp, color in COLORS.items():
            ax.hist(df[df['species'] == sp][feat], alpha=0.7, color=color,
                    label=sp, bins=15, edgecolor='white')
        ax.set_title(feat.replace(' (cm)', '').title(), fontweight='bold')
        ax.set_xlabel('Value (cm)', fontsize=9)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'eda_distributions.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[EDA] Saved {out}")


def plot_scatterplots(df: pd.DataFrame):
    pairs = [
        ('sepal length (cm)', 'sepal width (cm)'),
        ('petal length (cm)', 'petal width (cm)'),
        ('sepal length (cm)', 'petal length (cm)'),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    fig.suptitle('Feature Relationships by Species', fontsize=14, fontweight='bold')

    for ax, (x, y) in zip(axes, pairs):
        for sp, color in COLORS.items():
            sub = df[df['species'] == sp]
            ax.scatter(sub[x], sub[y], color=color, label=sp,
                       alpha=0.75, s=55, edgecolors='white', linewidth=0.5)
        ax.set_xlabel(x.replace(' (cm)', ''), fontsize=10)
        ax.set_ylabel(y.replace(' (cm)', ''), fontsize=10)
        ax.legend(fontsize=8)
        ax.grid(alpha=0.3)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'scatter_plots.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[EDA] Saved {out}")


def plot_boxplots(df: pd.DataFrame):
    feature_cols = [c for c in df.columns if c != 'species']
    fig, axes = plt.subplots(1, 4, figsize=(16, 5))
    fig.suptitle('Feature Spread per Species (Box Plots)', fontsize=14, fontweight='bold')

    for ax, feat in zip(axes, feature_cols):
        data_by_species = [df[df['species'] == sp][feat].values for sp in COLORS]
        bp = ax.boxplot(data_by_species, patch_artist=True, labels=list(COLORS.keys()))
        for patch, color in zip(bp['boxes'], COLORS.values()):
            patch.set_facecolor(color)
            patch.set_alpha(0.8)
        ax.set_title(feat.replace(' (cm)', '').title(), fontweight='bold', fontsize=10)
        ax.set_ylabel('cm', fontsize=9)
        ax.grid(axis='y', alpha=0.3)
        ax.set_xticklabels(list(COLORS.keys()), rotation=15, fontsize=8)

    plt.tight_layout()
    out = os.path.join(OUTPUT_DIR, 'boxplots.png')
    plt.savefig(out, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[EDA] Saved {out}")


if __name__ == '__main__':
    df = load_data()
    plot_distributions(df)
    plot_scatterplots(df)
    plot_boxplots(df)
    print("\n✅ EDA complete — check the outputs/ folder!")
