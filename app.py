import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="TCX3901 Freight Cost EDA", layout="wide")

@st.cache_data  # tells Streamlit "only reload the CSV if the file changes",
                # so the app doesn't reread 98,666 rows on every click
def load_data():
    return pd.read_csv('freight_cost_working_dataset.csv')

df = load_data()

st.title("Freight Cost EDA — TCX3901")
st.caption("Regression: predict freight value. Classification: flag disproportionately high freight (>30% of order value).")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Freight Share Distribution", "By Category", "Weight vs Freight", "By Route"]
)

with tab1:
    st.subheader("How is freight_share distributed?")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(df[df['freight_share'] < 2]['freight_share'], bins=80, color='#4C72B0')
    ax.axvline(0.30, color='red', linestyle='--', label='30% threshold')
    ax.axvline(df['freight_share'].median(), color='green', linestyle='--',
               label=f"median ({df['freight_share'].median():.2f})")
    ax.set_xlabel('Freight share'); ax.set_ylabel('Number of orders'); ax.legend()
    st.pyplot(fig)
    pct_above = (df['freight_share'] > 0.30).mean() * 100
    st.write(f"**{pct_above:.1f}%** of orders currently sit above the 30% threshold.")

with tab2:
    st.subheader("Freight share by product category")
    min_orders = st.slider("Minimum orders per category", 50, 1000, 200)
    cat = df.groupby('product_category_name')['freight_share'].agg(['median', 'count'])
    cat = cat[cat['count'] >= min_orders].sort_values('median', ascending=False)
    top_bottom = pd.concat([cat.head(6), cat.tail(5)])
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = ['#C44E52' if v in cat.head(6)['median'].values else '#55A868'
              for v in top_bottom['median']]
    ax.barh(top_bottom.index[::-1], top_bottom['median'][::-1], color=colors[::-1])
    ax.set_xlabel('Median freight_share')
    st.pyplot(fig)

with tab3:
    st.subheader("Does weight predict freight cost?")
    sample = df.sample(min(3000, len(df)), random_state=42)
    r = df['total_weight_g'].corr(df['order_freight'])
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.scatter(sample['total_weight_g'], sample['order_freight'], alpha=0.2, s=8, color='#4C72B0')
    ax.set_xlabel('Total order weight (g)'); ax.set_ylabel('Order freight (R$)')
    ax.set_xlim(0, 20000); ax.set_ylim(0, 150)
    st.pyplot(fig)
    st.write(f"Correlation coefficient: **{r:.2f}**")

with tab4:
    st.subheader("Median freight for the busiest routes")
    n_routes = st.slider("Number of routes to show", 5, 20, 10)
    route = df.groupby(['seller_state', 'customer_state'])['order_freight'].agg(['median', 'count'])
    route = route.sort_values('count', ascending=False).head(n_routes)
    labels = [f"{a}\u2192{b}" for a, b in route.index]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.barh(labels[::-1], route['median'][::-1], color='#8172B2')
    ax.set_xlabel('Median freight (R$)')
    st.pyplot(fig)
