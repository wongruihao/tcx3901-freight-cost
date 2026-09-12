import pandas as pd

orders = pd.read_csv('olist_orders_dataset.csv')
items = pd.read_csv('olist_order_items_dataset.csv')
customers = pd.read_csv('olist_customers_dataset.csv')
sellers = pd.read_csv('olist_sellers_dataset.csv')
products = pd.read_csv('olist_products_dataset.csv')

##Join at line-item level
df = items.merge(
    orders[['order_id', 'customer_id', 'order_status']],
    on='order_id', how='left'
)
df = df.merge(
    customers[['customer_id', 'customer_unique_id', 'customer_state', 'customer_city']],
    on='customer_id', how='left'
)
df = df.merge(
    sellers[['seller_id', 'seller_state', 'seller_city']],
    on='seller_id', how='left'
)
df = df.merge(
    products[['product_id', 'product_category_name', 'product_weight_g',
              'product_length_cm', 'product_height_cm', 'product_width_cm']],
    on='product_id', how='left'
)

print('Line-item rows after joining:', len(df))
print('Unique orders in that table:', df['order_id'].nunique())

##Collapse to one row per order with rule for every column
order_agg = df.groupby('order_id').agg(
    order_value=('price', 'sum'),
    order_freight=('freight_value', 'sum'),
    customer_unique_id=('customer_unique_id', 'first'),
    customer_state=('customer_state', 'first'),
    customer_city=('customer_city', 'first'),
    seller_state=('seller_state', 'first'),
    seller_state_nunique=('seller_state', 'nunique'),
    seller_id_nunique=('seller_id', 'nunique'),
    product_category_name=('product_category_name', 'first'),
    product_category_nunique=('product_category_name', 'nunique'),
    product_id_nunique=('product_id', 'nunique'),
    total_weight_g=('product_weight_g', 'sum'),
    total_length_cm=('product_length_cm', 'sum'),
    total_height_cm=('product_height_cm', 'sum'),
    total_width_cm=('product_width_cm', 'sum'),
    n_items=('order_item_id', 'count'),
).reset_index()

order_agg['is_multi_seller'] = order_agg['seller_id_nunique'] > 1
order_agg['is_multi_category'] = order_agg['product_category_nunique'] > 1
order_agg['is_multi_product'] = order_agg['product_id_nunique'] > 1
order_agg['freight_share'] = order_agg['order_freight'] / order_agg['order_value']

print('\n')
print('Order-level rows:', len(order_agg))

print('\n')
print('Multi-seller orders:', order_agg['is_multi_seller'].sum(),
      f"({order_agg['is_multi_seller'].mean()*100:.2f}%)")
print('Multi-category orders:', order_agg['is_multi_category'].sum(),
      f"({order_agg['is_multi_category'].mean()*100:.2f}%)")
print('Multi-product orders:', order_agg['is_multi_product'].sum(),
      f"({order_agg['is_multi_product'].mean()*100:.2f}%)")

print('\n')
print('Rows missing product_category_name:',
      order_agg['product_category_name'].isna().sum())
print('Rows missing customer_unique_id:',
      order_agg['customer_unique_id'].isna().sum())

##order_agg.to_csv('freight_cost_working_dataset_v2.csv', index=False)
