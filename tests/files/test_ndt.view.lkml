view: transaction_detail {
  derived_table: {
    explore_source: transactions {
      column: transaction_id {}
      column: customer_id {}
      column: channel_id {}
      column: gross_margin { field: transactions__line_items.gross_margin }
      column: product_id { field: transactions__line_items.product_id }
      column: store_id {}
      column: sale_price { field: transactions__line_items.sale_price }
      column: transaction_raw {}
      column: latitude { field: stores.latitude }
      column: longitude { field: stores.longitude }
      column: store_name { field: stores.name }
      column: store_state { field: stores.state }
      column: store_sq_ft { field: stores.sq_ft }
      column: brand { field: products.brand }
      column: category { field: products.category }
      column: department { field: products.department }
      column: area { field: products.area }
      column: product_name { field: products.name }
      column: sku { field: products.sku }
      column: channel_name { field: channels.name }
      column: traffic_source { field: customers.traffic_source }
      column: city { field: customers.city }
      column: country { field: customers.country }
      column: registered_date { field: customers.registered_date }
      column: email { field: customers.email }
      column: first_name { field: customers.first_name }
      column: gender { field: customers.gender }
      column: last_name { field: customers.last_name }
      column: address_latitude { field: customers.latitude }
      column: address_longitude { field: customers.longitude }
      column: state { field: customers.state }
      column: postcode { field: customers.postcode }
      column: customer_average_basket_size { field: customer_facts.customer_average_basket_size }
      column: customer_lifetime_gross_margin { field: customer_facts.customer_lifetime_gross_margin }
      column: customer_lifetime_sales { field: customer_facts.customer_lifetime_sales }
      column: customer_lifetime_transactions { field: customer_facts.customer_lifetime_transactions }
      column: customer_lifetime_quantity { field: customer_facts.customer_lifetime_quantity }
      column: customer_first_purchase_date { field: customer_facts.customer_first_purchase_date }
    }
#     datagroup_trigger: daily
#     partition_keys: ["transaction_raw"]
#     cluster_keys: ["store_name"]
  }

dimension: customer_first_purchase_date {}
dimension: customer_lifetime_quantity {}

}