import os
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from db import get_medicines_data


# ---------- Design tokens (kept in sync with static/css/style.css) ----------

COLOR_BG = '#F6F8F5'
COLOR_SURFACE = '#FFFFFF'
COLOR_INK = '#16241F'
COLOR_PRIMARY = '#1F5745'
COLOR_PRIMARY_LIGHT = '#2F7A63'
COLOR_GOLD = '#D9A441'
COLOR_GOLD_DARK = '#B8842B'
COLOR_ALERT = '#C1483D'
COLOR_MUTED = '#6B7B74'
COLOR_BORDER = '#DCE5DD'

# Sequential green palette for bar/box charts ranked by volume
GREEN_SEQUENCE = ['#1F5745', '#2F7A63', '#4C9A82', '#7CB99F', '#A9D3BF', '#CFE7DC']


def apply_theme():
    """ Apply a shared visual theme across every chart so they match the web UI. """
    sns.set_theme(style='whitegrid')

    plt.rcParams.update({
        'figure.facecolor': COLOR_BG,
        'axes.facecolor': COLOR_SURFACE,
        'savefig.facecolor': COLOR_BG,
        'axes.edgecolor': COLOR_BORDER,
        'axes.labelcolor': COLOR_INK,
        'text.color': COLOR_INK,
        'xtick.color': COLOR_MUTED,
        'ytick.color': COLOR_MUTED,
        'grid.color': COLOR_BORDER,
        'grid.linewidth': 0.6,
        'axes.titlecolor': COLOR_INK,
        'axes.titleweight': 'bold',
        'axes.titlesize': 14,
        'axes.titlelocation': 'left',
        'axes.titlepad': 14,
        'font.family': 'sans-serif',
        'font.sans-serif': ['IBM Plex Sans', 'DejaVu Sans', 'Arial'],
        'axes.spines.top': False,
        'axes.spines.right': False,
    })


BASE_RESULTS_DIR = 'Diagramatic Results'  # Dir. for saving diagrams
os.makedirs(BASE_RESULTS_DIR, exist_ok=True)

run_timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
FILE_DIR = os.path.join(BASE_RESULTS_DIR, run_timestamp)
os.makedirs(FILE_DIR, exist_ok=True)


def save_plot(filename):
    """ Save the current matplotlib figure into the timestamped run folder """
    filepath = os.path.join(FILE_DIR, filename)
    plt.savefig(filepath, bbox_inches='tight', dpi=300)
    plt.close()
    print(f'Saved to {filepath}')


# ---------- Reading Input ----------

def read_from_db():
    """ Read the medicines table from the database """
    print('---- Reading from database ----\n')

    result = get_medicines_data()

    if result['error'] is not None:
        raise RuntimeError(f"Failed to read from database: {result['error']}")

    if not result['rows']:
        raise RuntimeError("No rows returned from medicines table.")

    data = pd.DataFrame(result['rows'])

    print('\n File Head : ')
    print(data.head())
    print('\n---- Describe data : ')
    print(data.describe(include='all'), end='\n\n')

    print('\n---- Data info : ')
    print(data.info(), end='\n\n')

    return data


# ---------- Cleaning / prep ----------

def prepare_data(data):
    data['price'] = pd.to_numeric(data['price'], errors='coerce')
    data['short_composition1'] = data['short_composition1'].fillna('')
    data['short_composition2'] = data['short_composition2'].fillna('')

    data['composition_key'] = data.apply(
        lambda r: ' + '.join(sorted(filter(None, [r['short_composition1'].strip(),
                                                    r['short_composition2'].strip()]))),
        axis=1
    )
    return data


# ---------- Visual Analysis - Plotting ----------

def make_plot(data):
    apply_theme()

    # 1. Overall price distribution (clipped to 99th percentile to avoid extreme outliers squashing the plot)
    price_cap = data['price'].quantile(0.99)
    plt.figure(figsize=(12, 6))
    sns.histplot(data[data['price'] <= price_cap]['price'], bins=50, kde=True,
                 color=COLOR_PRIMARY_LIGHT, edgecolor=COLOR_BG, alpha=0.85,
                 line_kws={'color': COLOR_GOLD_DARK, 'linewidth': 2})
    plt.title('Price Distribution of Medicines (up to 99th percentile)')
    plt.xlabel('Price (₹)')
    plt.ylabel('Number of Medicines')
    save_plot('01_price_distribution.png')

    # 2. Price by top 10 medicine types
    plt.figure(figsize=(14, 6))
    top_types = data['type'].value_counts().head(10).index
    sns.boxplot(data=data[data['type'].isin(top_types)], x='type', y='price',
                color=COLOR_PRIMARY_LIGHT,
                boxprops={'edgecolor': COLOR_PRIMARY, 'alpha': 0.85},
                medianprops={'color': COLOR_GOLD_DARK, 'linewidth': 2},
                whiskerprops={'color': COLOR_MUTED},
                capprops={'color': COLOR_MUTED},
                flierprops={'markerfacecolor': COLOR_ALERT, 'markeredgecolor': COLOR_ALERT, 'markersize': 3, 'alpha': 0.5})
    plt.title('Price Distribution — Top 10 Medicine Types')
    plt.xlabel('')
    plt.ylabel('Price (₹)')
    plt.xticks(rotation=45, ha='right')
    plt.ylim(0, price_cap)
    save_plot('02_price_by_type_boxplot.png')

    # 3. Top 10 manufacturers by number of listed medicines
    plt.figure(figsize=(12, 6))
    top_manufacturers = data['manufacturer_name'].value_counts().head(10)
    sns.barplot(x=top_manufacturers.values, y=top_manufacturers.index, orient='h',
                palette=GREEN_SEQUENCE, hue=top_manufacturers.index, legend=False)
    plt.title('Top 10 Manufacturers by Number of Medicines')
    plt.xlabel('Number of Medicines')
    plt.ylabel('')
    save_plot('03_top_manufacturers.png')

    # 4. Compositions with the most branded variants (competing brands)
    plt.figure(figsize=(12, 6))
    top_compositions = data[data['composition_key'] != '']['composition_key'].value_counts().head(10)
    sns.barplot(x=top_compositions.values, y=top_compositions.index, orient='h',
                color=COLOR_GOLD, edgecolor=COLOR_GOLD_DARK)
    plt.title('Top 10 Compositions by Number of Competing Brands')
    plt.xlabel('Number of Branded Variants')
    plt.ylabel('')
    save_plot('04_top_compositions.png')

    # 5. Discontinued vs active medicines
    plt.figure(figsize=(6, 6))
    counts = data['is_discontinued'].astype(bool).value_counts().rename({True: 'Discontinued', False: 'Active'})
    colors = [COLOR_PRIMARY if label == 'Active' else COLOR_ALERT for label in counts.index]
    wedges, _, autotexts = plt.pie(
        counts.values, labels=counts.index, autopct='%1.1f%%',
        colors=colors, wedgeprops={'edgecolor': COLOR_BG, 'linewidth': 2},
        textprops={'color': COLOR_INK}
    )
    for autotext in autotexts:
        autotext.set_color('#FFFFFF')
        autotext.set_fontweight('bold')
    plt.title('Active vs Discontinued Medicines')
    save_plot('05_discontinued_pie.png')

    # 6. Medicine type distribution (top 10)
    plt.figure(figsize=(12, 6))
    top_type_counts = data['type'].value_counts().head(10)
    sns.barplot(x=top_type_counts.values, y=top_type_counts.index, orient='h',
                palette=GREEN_SEQUENCE, hue=top_type_counts.index, legend=False)
    plt.title('Top 10 Medicine Types by Count')
    plt.xlabel('Number of Medicines')
    plt.ylabel('')
    save_plot('06_type_distribution.png')


# ---------- Savings potential summary ----------

def savings_summary(data):
    savings_rows = []
    grouped = data[data['composition_key'] != ''].groupby('composition_key')
    for key, group in grouped:
        if len(group) > 1:
            max_price = group['price'].max()
            min_price = group['price'].min()
            if pd.notna(max_price) and pd.notna(min_price):
                savings_rows.append(max_price - min_price)

    if savings_rows:
        avg_savings = sum(savings_rows) / len(savings_rows)
        print(f'\n---- Savings Potential Summary ----')
        print(f'Composition groups with multiple brands: {len(savings_rows)}')
        print(f'Average potential saving per group: ₹{avg_savings:.2f}\n')
    else:
        print('\nNot enough data to compute savings potential.\n')


# ---------- Flow function ----------

def main():
    data = read_from_db()
    data = prepare_data(data)
    make_plot(data)
    savings_summary(data)
    print(f'\nAll charts saved in: {FILE_DIR}')


if __name__ == '__main__':
    main()