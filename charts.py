import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('freight_cost_working_dataset.csv')

##---------------------------------------------------------------
##Chart 1: how is freight_share distributed across all orders?
##---------------------------------------------------------------

fig, ax = plt.subplots(figsize=(6, 4))
ax.hist(df[df['freight_share'] < 2]['freight_share'], bins=80,
        color='#4C72B0', edgecolor='none')
ax.axvline(0.30, color='red', linestyle='--', label='30% threshold')
ax.axvline(df['freight_share'].median(), color='green', linestyle='--',
           label=f"median ({df['freight_share'].median():.2f})")
ax.set_xlabel('Freight share (freight_value / order_value)')
ax.set_ylabel('Number of orders')
ax.set_title('Distribution of freight_share')
ax.legend()
plt.tight_layout()
plt.savefig('chart1_freight_share_dist.png', dpi=130)
plt.close()

##---------------------------------------------------------------
##Chart 2: which product categories have the highest freight_share?
##---------------------------------------------------------------

cat = df.groupby('product_category_name')['freight_share'].agg(['median', 'count'])
cat = cat[cat['count'] >= 200].sort_values('median', ascending=False)
top_bottom = pd.concat([cat.head(6), cat.tail(5)])  # 6 highest + 5 lowest

fig, ax = plt.subplots(figsize=(6, 4.5))
colors = ['#C44E52' if v in cat.head(6)['median'].values else '#55A868'
          for v in top_bottom['median']]
ax.barh(top_bottom.index[::-1], top_bottom['median'][::-1], color=colors[::-1])
ax.set_xlabel('Median freight_share')
ax.set_title('Freight share by product category\n(highest in red, lowest in green, min 200 orders)')
plt.tight_layout()
plt.savefig('chart2_freight_by_category.png', dpi=130)
plt.close()

##---------------------------------------------------------------
##Chart 3: does a heavier order cost more to ship?
##---------------------------------------------------------------

sample = df.sample(3000, random_state=42)
r = df['total_weight_g'].corr(df['order_freight'])  

fig, ax = plt.subplots(figsize=(6, 4))
ax.scatter(sample['total_weight_g'], sample['order_freight'],
           alpha=0.2, s=8, color='#4C72B0') 
ax.set_xlabel('Total order weight (g)')
ax.set_ylabel('Order freight (R$)')
ax.set_title(f'Weight vs freight (r = {r:.2f}, n=3,000 sample)')
ax.set_xlim(0, 20000)
ax.set_ylim(0, 150)
plt.tight_layout()
plt.savefig('chart3_weight_vs_freight.png', dpi=130)
plt.close()

##---------------------------------------------------------------
##Chart 4: which shipping routes cost the most, among the busiest ones?
##---------------------------------------------------------------

route = df.groupby(['seller_state', 'customer_state'])['order_freight'].agg(['median', 'count'])
route = route.sort_values('count', ascending=False).head(10)  # top 10 busiest routes only
labels = [f"{a}\u2192{b}" for a, b in route.index]

fig, ax = plt.subplots(figsize=(6, 4.5))
ax.barh(labels[::-1], route['median'][::-1], color='#8172B2')
ax.set_xlabel('Median freight (R$)')
ax.set_title('Median freight for the 10 highest-volume routes')
plt.tight_layout()
plt.savefig('chart4_route_freight.png', dpi=130)
plt.close()

