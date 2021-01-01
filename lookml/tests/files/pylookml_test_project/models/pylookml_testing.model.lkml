connection: "disco-parsec"

label: " eCommerce"
include: "queries*.view" # includes all queries refinements
include: "/views/**/*.view" # include all the views
include: "/dashboards/*.dashboard.lookml" # include all the views


############ Model Configuration #############

datagroup: ecommerce_etl {
  sql_trigger: SELECT max(created_at) FROM ecomm.events ;;
  max_cache_age: "24 hours"
}

persist_with: ecommerce_etl
############ Base Explores #############

explore: order_items {
  label: "(1) Orders, Items and Users"
  view_name: order_items

  join: order_facts {
    type: left_outer
    view_label: "Orders"
    relationship: many_to_one
    sql_on: ${order_facts.order_id} = ${order_items.order_id} ;;
  }

  join: inventory_items {
    #Left Join only brings in items that have been sold as order_item
    type: full_outer
    relationship: one_to_one
    sql_on: ${inventory_items.id} = ${order_items.inventory_item_id} ;;
  }

  join: users {
    type: left_outer
    relationship: many_to_one
    sql_on: ${order_items.user_id} = ${users.id} ;;
  }

  join: user_order_facts {
    view_label: "Users"
    type: left_outer
    relationship: many_to_one
    sql_on: ${user_order_facts.user_id} = ${order_items.user_id} ;;
  }

  join: products {
    type: left_outer
    relationship: many_to_one
    sql_on: ${products.id} = ${inventory_items.product_id} ;;
  }

  join: repeat_purchase_facts {
    relationship: many_to_one
    type: full_outer
    sql_on: ${order_items.order_id} = ${repeat_purchase_facts.order_id} ;;
  }

  join: distribution_centers {
    type: left_outer
    sql_on: ${distribution_centers.id} = ${inventory_items.product_distribution_center_id} ;;
    relationship: many_to_one
  }
}


#########  Event Data Explores #########

explore: events {
  label: "(2) Web Event Data"

  join: sessions {
    type: left_outer
    sql_on: ${events.session_id} =  ${sessions.session_id} ;;
    relationship: many_to_one
  }

  join: session_landing_page {
    from: events
    type: left_outer
    sql_on: ${sessions.landing_event_id} = ${session_landing_page.event_id} ;;
    fields: [simple_page_info*]
    relationship: one_to_one
  }

  join: session_bounce_page {
    from: events
    type: left_outer
    sql_on: ${sessions.bounce_event_id} = ${session_bounce_page.event_id} ;;
    fields: [simple_page_info*]
    relationship: many_to_one
  }

  join: product_viewed {
    from: products
    type: left_outer
    sql_on: ${events.viewed_product_id} = ${product_viewed.id} ;;
    relationship: many_to_one
  }

  join: users {
    type: left_outer
    sql_on: ${sessions.session_user_id} = ${users.id} ;;
    relationship: many_to_one
  }

  join: user_order_facts {
    type: left_outer
    sql_on: ${users.id} = ${user_order_facts.user_id} ;;
    relationship: one_to_one
    view_label: "Users"
  }
}

explore: sessions {
  label: "(3) Web Session Data"

  join: events {
    type: left_outer
    sql_on: ${sessions.session_id} = ${events.session_id} ;;
    relationship: one_to_many
  }

  join: product_viewed {
    from: products
    type: left_outer
    sql_on: ${events.viewed_product_id} = ${product_viewed.id} ;;
    relationship: many_to_one
  }

  join: session_landing_page {
    from: events
    type: left_outer
    sql_on: ${sessions.landing_event_id} = ${session_landing_page.event_id} ;;
    fields: [session_landing_page.simple_page_info*]
    relationship: one_to_one
  }

  join: session_bounce_page {
    from: events
    type: left_outer
    sql_on: ${sessions.bounce_event_id} = ${session_bounce_page.event_id} ;;
    fields: [session_bounce_page.simple_page_info*]
    relationship: one_to_one
  }

  join: users {
    type: left_outer
    relationship: many_to_one
    sql_on: ${users.id} = ${sessions.session_user_id} ;;
  }

  join: user_order_facts {
    type: left_outer
    relationship: many_to_one
    sql_on: ${user_order_facts.user_id} = ${users.id} ;;
    view_label: "Users"
  }
}


#########  Advanced Extensions #########

explore: affinity {
  label: "(4) Affinity Analysis"

  always_filter: {
    filters: {
      field: affinity.product_b_id
      value: "-NULL"
    }
  }

  join: product_a {
    from: products
    type: left_outer
    view_label: "Product A Details"
    relationship: many_to_one
    sql_on: ${affinity.product_a_id} = ${product_a.id} ;;
  }

  join: product_b {
    from: products
    type: left_outer
    view_label: "Product B Details"
    relationship: many_to_one
    sql_on: ${affinity.product_b_id} = ${product_b.id} ;;
  }
}

explore: orders_with_share_of_wallet_application {
  label: "(5) Share of Wallet Analysis"
  extends: [order_items]
  view_name: order_items

  join: order_items_share_of_wallet {
    view_label: "Share of Wallet"
  }
}

explore: journey_mapping {
  label: "(6) Customer Journey Mapping"
  extends: [order_items]
  view_name: order_items

  join: repeat_purchase_facts {
    relationship: many_to_one
    sql_on: ${repeat_purchase_facts.next_order_id} = ${order_items.order_id} ;;
    type: left_outer
  }

  join: next_order_items {
    type: left_outer
    from: order_items
    sql_on: ${repeat_purchase_facts.next_order_id} = ${next_order_items.order_id} ;;
    relationship: many_to_many
  }

  join: next_order_inventory_items {
    type: left_outer
    from: inventory_items
    relationship: many_to_one
    sql_on: ${next_order_items.inventory_item_id} = ${next_order_inventory_items.id} ;;
  }

  join: next_order_products {
    from: products
    type: left_outer
    relationship: many_to_one
    sql_on: ${next_order_inventory_items.product_id} = ${next_order_products.id} ;;
  }
}

explore: inventory_snapshot {
  label: "(7) Historical Stock Snapshot Analysis"
  join: trailing_sales_snapshot {
    sql_on: ${inventory_snapshot.product_id}=${trailing_sales_snapshot.product_id}
      AND ${inventory_snapshot.snapshot_date}=${trailing_sales_snapshot.snapshot_date};;
    type: left_outer
    relationship: one_to_one
  }

  join: products {
    type: left_outer
    sql_on: ${inventory_snapshot.product_id} = ${products.id} ;;
    relationship: many_to_one
  }

  join: distribution_centers {
    type: left_outer
    sql_on: ${products.distribution_center_id}=${distribution_centers.id} ;;
    relationship: many_to_one
  }
}


explore: kitten_order_items {
  label: "Order Items (Kittens)"
  hidden: yes
  extends: [order_items]

  join: users {
    view_label: "Kittens"
    from: kitten_users
  }
}
