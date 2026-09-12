import pandas as pd

df = pd.read_csv('freight_cost_working_dataset.csv')

##---------------------------------------------------------------
##Regression baseline 1: global median
##---------------------------------------------------------------

global_median = df['order_freight'].median()
mae_global = (df['order_freight'] - global_median).abs().mean()

##---------------------------------------------------------------
##Regression baseline 2: route median (stronger baseline)
##---------------------------------------------------------------

route_median = df.groupby(['seller_state', 'customer_state'])['order_freight'] \
                  .transform('median')
mae_route = (df['order_freight'] - route_median).abs().mean()
n_routes = df.groupby(['seller_state', 'customer_state']).ngroups

##---------------------------------------------------------------
##Classification baseline: majority class
##---------------------------------------------------------------

pct_high_freight = (df['freight_share'] > 0.30).mean() * 100
majority_accuracy = max(pct_high_freight, 100 - pct_high_freight)



print(f"Global median freight:      R${global_median:.2f}")
print(f"MAE (global median):        R${mae_global:.2f}")
print(f"Distinct routes:            {n_routes}")
print(f"MAE (route median):         R${mae_route:.2f}")
print(f"% high-freight orders:      {pct_high_freight:.2f}%")
print(f"Majority-class accuracy:    {majority_accuracy:.2f}%")
