- dashboard: brand_lookup
  title: Brand Lookup
  layout: newspaper
  preferred_viewer: dashboards-next
  query_timezone: user_timezone
  embed_style:
    background_color: "#f6f8fa"
    show_title: true
    title_color: "#3a4245"
    show_filters_bar: true
    tile_text_color: "#3a4245"
    tile_separator_color: "#faf3f3"
    tile_border_radius: 5
    show_tile_shadow: false
    text_tile_text_color: "#556d7a"
  elements:
  - title: Total Orders
    name: Total Orders
    model: thelook
    explore: order_items
    type: single_value
    fields: [order_items.order_count]
    filters: {}
    sorts: [order_items.order_count desc]
    limit: 500
    query_timezone: America/Los_Angeles
    font_size: medium
    text_color: black
    listen:
      Brand Name: products.brand
      Date: order_items.created_date
      State: users.state
    row: 2
    col: 8
    width: 4
    height: 3
  - title: Total Customers
    name: Total Customers
    model: thelook
    explore: order_items
    type: single_value
    fields: [users.count]
    filters: {}
    sorts: [users.count desc]
    limit: 500
    query_timezone: America/Los_Angeles
    font_size: medium
    text_color: black
    note_state: expanded
    note_display: hover
    note_text: I've added a note
    listen:
      Brand Name: products.brand
      Date: order_items.created_date
      State: users.state
    row: 2
    col: 0
    width: 4
    height: 3
  - title: Average Order Value
    name: Average Order Value
    model: thelook
    explore: order_items
    type: single_value
    fields: [order_items.average_sale_price]
    filters: {}
    sorts: [order_items.average_sale_price desc]
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    font_size: medium
    text_color: black
    note_state: collapsed
    note_display: below
    note_text: ''
    listen:
      Brand Name: products.brand
      Date: order_items.created_date
      State: users.state
    row: 2
    col: 4
    width: 4
    height: 3
  - title: Brand Traffic by Source, OS
    name: Brand Traffic by Source, OS
    model: thelook
    explore: events
    type: looker_donut_multiples
    fields: [users.traffic_source, events.os, events.count]
    pivots: [users.traffic_source]
    filters:
      users.traffic_source: "-NULL"
    sorts: [events.count desc 1, users.traffic_source]
    limit: 20
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_value_labels: true
    font_size: 12
    colors: ["#64518A", "#8D7FB9", "#EA8A2F", "#F2B431", "#2DA5DE", "#57BEBE", "#7F7977",
      "#B2A898", "#494C52"]
    color_application:
      collection_id: google
      palette_id: google-categorical-0
      options:
        steps: 5
        reverse: false
    series_colors: {}
    show_view_names: true
    stacking: ''
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    x_axis_scale: auto
    show_null_labels: false
    defaults_version: 1
    note_state: collapsed
    note_display: above
    note_text: ''
    listen:
      Brand Name: product_viewed.brand
      Date: events.event_date
      State: users.state
    row: 28
    col: 14
    width: 10
    height: 11
  - title: Top Product Categories - Cart vs Conversion
    name: Top Product Categories - Cart vs Conversion
    model: thelook
    explore: events
    type: looker_column
    fields: [product_viewed.category, sessions.overall_conversion, sessions.cart_to_checkout_conversion,
      sessions.count_cart_or_later]
    filters:
      product_viewed.category: "-NULL"
    sorts: [sessions.count_cart_or_later desc]
    limit: 8
    column_limit: 50
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: false
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: circle_outline
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: false
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    color_application:
      collection_id: google
      palette_id: google-categorical-0
      options:
        steps: 5
        reverse: false
    y_axes: [{label: Total Added to Cart, maxValue: !!null '', minValue: !!null '',
        orientation: left, showLabels: true, showValues: true, tickDensity: default,
        tickDensityCustom: 5, type: linear, unpinAxis: false, valueFormat: !!null '',
        series: [{id: sessions.count_cart_or_later, name: "(4) Add to Cart or later"}]},
      {label: '', maxValue: !!null '', minValue: !!null '', orientation: right, showLabels: true,
        showValues: true, tickDensity: default, tickDensityCustom: 5, type: linear,
        unpinAxis: false, valueFormat: !!null '', series: [{id: sessions.overall_conversion,
            name: Overall Conversion}, {id: sessions.cart_to_checkout_conversion,
            name: Cart to Checkout Conversion}]}]
    y_axis_labels: [Cart to Checkout Conversion Percent, Total Added to Cart]
    hide_legend: false
    colors: ["#64518A", "#8D7FB9"]
    series_types:
      sessions.cart_to_checkout_conversion: line
      sessions.overall_conversion: line
    series_colors: {}
    series_labels:
      sessions.cart_to_checkout_conversion: Cart to Checkout Conversion
      sessions.overall_conversion: Overall Conversion
      sessions.count_cart_or_later: "# of Add to Cart Events"
    y_axis_orientation: [right, left]
    x_axis_label_rotation: -45
    label_rotation: 0
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    listen:
      Brand Name: product_viewed.brand
      Date: events.event_date
      State: users.state
    row: 28
    col: 0
    width: 14
    height: 6
  - title: Top Visitors and Transaction History
    name: Top Visitors and Transaction History
    model: thelook
    explore: events
    type: looker_grid
    fields: [users.name, users.email, users.state, users.traffic_source, sessions.count]
    filters:
      users.name: "-NULL"
    sorts: [sessions.count desc]
    limit: 15
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: true
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    series_cell_visualizations:
      sessions.count:
        is_active: false
    table_theme: gray
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    conditional_formatting_ignored_fields: []
    truncate_column_names: false
    series_types: {}
    listen:
      Brand Name: product_viewed.brand
      Date: events.event_date
      State: users.state
    row: 42
    col: 12
    width: 12
    height: 8
  - title: Sales and Sale Price Trend
    name: Sales and Sale Price Trend
    model: thelook
    explore: order_items
    type: looker_line
    fields: [order_items.created_date, order_items.total_sale_price, order_items.average_sale_price]
    filters: {}
    sorts: [order_items.total_sale_price desc]
    limit: 500
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: false
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: false
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: false
    show_null_points: true
    interpolation: monotone
    color_application:
      collection_id: google
      palette_id: google-categorical-0
      options:
        steps: 5
    y_axis_labels: [Total Sale Amount, Average Selling Price]
    x_axis_label: Order Date
    hide_legend: true
    colors: ["#F2B431", "#57BEBE"]
    series_colors: {}
    y_axis_orientation: [left, right]
    x_axis_datetime: true
    hide_points: true
    color_palette: Custom
    defaults_version: 1
    note_state: collapsed
    note_display: hover
    note_text: ''
    listen:
      Brand Name: products.brand
      Date: order_items.created_date
      State: users.state
    row: 2
    col: 12
    width: 12
    height: 7
  - title: Top Purchasers of Brand
    name: Top Purchasers of Brand
    model: thelook
    explore: order_items
    type: looker_grid
    fields: [users.name, users.email, order_items.count, order_items.total_sale_price,
      users.state]
    filters: {}
    sorts: [order_items.count desc]
    limit: 15
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    truncate_column_names: false
    hide_totals: false
    hide_row_totals: false
    table_theme: gray
    limit_displayed_rows: false
    enable_conditional_formatting: false
    conditional_formatting_ignored_fields: []
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    series_types: {}
    listen:
      Brand Name: products.brand
      Date: order_items.created_date
      State: users.state
    row: 42
    col: 0
    width: 12
    height: 8
  - title: Website Sessions by Hour of Day and User Lifetime Order Tier
    name: Website Sessions by Hour of Day and User Lifetime Order Tier
    model: thelook
    explore: events
    type: looker_column
    fields: [user_order_facts.lifetime_orders_tier, sessions.count, events.event_hour_of_day]
    pivots: [user_order_facts.lifetime_orders_tier]
    fill_fields: [events.event_hour_of_day]
    filters: {}
    sorts: [user_order_facts.lifetime_orders_tier 0, events.event_hour_of_day]
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: false
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: normal
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    color_application:
      collection_id: google
      palette_id: google-categorical-0
      options:
        steps: 5
        reverse: false
    hidden_series: [Undefined]
    colors: ["#2DA5DE", "#57BEBE", "#EA8A2F", "#F2B431", "#64518A", "#8D7FB9", "#7F7977",
      "#B2A898", "#494C52"]
    series_colors: {}
    series_labels:
      '1': 1 Lifetime Purchase
      1 - 2 - sessions.count: '1'
    show_null_points: true
    interpolation: linear
    defaults_version: 1
    note_state: collapsed
    note_display: hover
    note_text: These are order totals by hour of day
    listen:
      Brand Name: product_viewed.brand
      Date: events.event_date
      State: users.state
    row: 34
    col: 0
    width: 14
    height: 5
  - title: Most Correlated Items
    name: Most Correlated Items
    model: thelook
    explore: affinity
    type: looker_grid
    fields: [product_a.item_name, product_b.item_name, affinity.avg_order_affinity,
      affinity.avg_user_affinity]
    filters:
      affinity.product_b_id: "-NULL"
      affinity.avg_order_affinity: NOT NULL
      product_b.brand: '"Levi''s"'
    sorts: [affinity.avg_order_affinity desc]
    limit: 15
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    table_theme: white
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    color_application:
      collection_id: b43731d5-dc87-4a8e-b807-635bef3948e7
      palette_id: fb7bb53e-b77b-4ab6-8274-9d420d3d73f3
      options:
        steps: 5
        reverse: false
    series_cell_visualizations:
      affinity.avg_order_affinity:
        is_active: true
        palette:
          palette_id: 14bc3e56-1edb-5cb6-143e-bc3c0d49dc0f
          collection_id: b43731d5-dc87-4a8e-b807-635bef3948e7
          custom_colors:
          - "#f20265"
          - "#FFD95F"
          - "#72D16D"
      affinity.avg_user_affinity:
        is_active: true
        palette:
          palette_id: 8182e447-1db4-af27-fe8f-0cc57a1b4132
          collection_id: b43731d5-dc87-4a8e-b807-635bef3948e7
          custom_colors:
          - "#f20265"
          - "#FFD95F"
          - "#72D16D"
    stacking: ''
    trellis: ''
    colors: ["#57BEBE", "#EA8A2F", "#F2B431", "#64518A", "#8D7FB9", "#7F7977", "#B2A898",
      "#494C52"]
    show_value_labels: false
    label_density: 25
    legend_position: center
    x_axis_gridlines: false
    y_axis_gridlines: true
    point_style: circle_outline
    hidden_series: [product_a.count, product_b.count]
    y_axis_combined: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    x_axis_scale: auto
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    show_null_points: true
    interpolation: linear
    ordering: none
    show_null_labels: false
    color_palette: Custom
    hidden_fields: []
    series_types: {}
    defaults_version: 1
    listen:
      Brand Name: product_a.brand
    row: 18
    col: 0
    width: 14
    height: 8
  - title: Purchasers of This Brand Also Bought (Brand Affinity)
    name: Purchasers of This Brand Also Bought (Brand Affinity)
    model: thelook
    explore: affinity
    type: looker_grid
    fields: [product_a.brand, product_b.brand, affinity.avg_order_affinity, affinity.avg_user_affinity,
      affinity.combined_affinity]
    filters:
      affinity.product_b_id: "-NULL"
      affinity.avg_order_affinity: NOT NULL
    sorts: [affinity.combined_affinity desc]
    limit: 15
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: true
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    series_labels:
      product_b.brand: Brand Name
    series_cell_visualizations:
      affinity.avg_order_affinity:
        is_active: true
        palette:
          palette_id: 17151457-0425-49e1-f2ab-69c3b7658883
          collection_id: f14810d2-98d7-42df-82d0-bc185a074e42
          custom_colors:
          - "#f20265"
          - "#FFD95F"
          - "#72D16D"
      affinity.avg_user_affinity:
        is_active: true
        palette:
          palette_id: 2c7c9b87-e295-002c-4f6f-d50381deac58
          collection_id: f14810d2-98d7-42df-82d0-bc185a074e42
          custom_colors:
          - "#f20265"
          - "#FFD95F"
          - "#72D16D"
    table_theme: gray
    limit_displayed_rows: false
    enable_conditional_formatting: false
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    conditional_formatting_ignored_fields: []
    stacking: ''
    show_value_labels: false
    label_density: 25
    legend_position: center
    x_axis_gridlines: false
    y_axis_gridlines: true
    y_axis_combined: true
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    x_axis_scale: auto
    ordering: none
    show_null_labels: false
    hidden_fields: [affinity.combined_affinity, product_a.brand]
    truncate_column_names: false
    series_types: {}
    listen:
      Brand Name: product_a.brand
    row: 18
    col: 14
    width: 10
    height: 8
  - title: Brand Share of Wallet over Customer Lifetime
    name: Brand Share of Wallet over Customer Lifetime
    model: thelook
    explore: orders_with_share_of_wallet_application
    type: looker_line
    fields: [order_items.months_since_signup, order_items_share_of_wallet.brand_share_of_wallet_within_company,
      order_items_share_of_wallet.total_sale_price_brand_v2]
    filters:
      order_items.months_since_signup: "<=18"
    sorts: [order_items.months_since_signup]
    limit: 500
    query_timezone: America/Los_Angeles
    x_axis_gridlines: false
    y_axis_gridlines: false
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: ''
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    show_null_points: true
    interpolation: monotone
    color_application:
      collection_id: google
      palette_id: google-categorical-0
      options:
        steps: 5
        reverse: false
    y_axes: [{label: '', orientation: left, series: [{id: order_items_share_of_wallet.brand_share_of_wallet_within_company,
            name: Brand Share of Wallet Within Company, axisId: order_items_share_of_wallet.brand_share_of_wallet_within_company}],
        showLabels: true, showValues: true, unpinAxis: false, tickDensity: default,
        tickDensityCustom: 5, type: linear}, {label: !!null '', orientation: right,
        series: [{id: order_items_share_of_wallet.total_sale_price_brand_v2, name: Total
              Sales - This Brand, axisId: order_items_share_of_wallet.total_sale_price_brand_v2}],
        showLabels: true, showValues: true, unpinAxis: false, tickDensity: default,
        tickDensityCustom: 5, type: linear}]
    series_types: {}
    series_colors: {}
    defaults_version: 1
    listen:
      Brand Name: order_items_share_of_wallet.brand
      Date: order_items.created_date
      State: users.state
    row: 9
    col: 12
    width: 12
    height: 6
  - title: Most Popular Categories
    name: Most Popular Categories
    model: thelook
    explore: order_items
    type: looker_column
    fields: [products.category, products.department, order_items.total_sale_price]
    pivots: [products.department]
    sorts: [products.department 0, order_items.total_sale_price desc 2]
    limit: 500
    column_limit: 50
    row_total: right
    query_timezone: user_timezone
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
    show_y_axis_labels: true
    show_y_axis_ticks: true
    y_axis_tick_density: default
    y_axis_tick_density_custom: 5
    show_x_axis_label: true
    show_x_axis_ticks: true
    y_axis_scale_mode: linear
    x_axis_reversed: false
    y_axis_reversed: false
    plot_size_by_field: false
    trellis: ''
    stacking: normal
    limit_displayed_rows: false
    legend_position: center
    point_style: none
    show_value_labels: false
    label_density: 25
    x_axis_scale: auto
    y_axis_combined: true
    ordering: none
    show_null_labels: false
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    color_application:
      collection_id: google
      palette_id: google-categorical-0
      options:
        steps: 5
    series_types: {}
    show_row_numbers: true
    truncate_column_names: false
    hide_totals: false
    hide_row_totals: false
    table_theme: gray
    enable_conditional_formatting: false
    conditional_formatting_ignored_fields: []
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    defaults_version: 1
    listen: {}
    row: 5
    col: 0
    width: 12
    height: 10
  - name: "<span class='fa fa-dollar'> Brand Overview </span>"
    type: text
    title_text: "<span class='fa fa-dollar'> Brand Overview </span>"
    subtitle_text: What are the high level revenue metrics for this brand?
    row: 0
    col: 0
    width: 24
    height: 2
  - name: "<span class='fa fa-heart'> Affinity Analysis </span>"
    type: text
    title_text: "<span class='fa fa-heart'> Affinity Analysis </span>"
    subtitle_text: What products and brands have the highest affinity?
    body_text: "**Recommended Action** Plan advertising campaign to recommend products\
      \ to users based on affinity"
    row: 15
    col: 0
    width: 24
    height: 3
  - name: "<span class='fa fa-laptop'> Web Analytics </span>"
    type: text
    title_text: "<span class='fa fa-laptop'> Web Analytics </span>"
    subtitle_text: How are users interacting with our website?
    row: 26
    col: 0
    width: 24
    height: 2
  - name: "<span class='fa fa-users'> Top Customers </span>"
    type: text
    title_text: "<span class='fa fa-users'> Top Customers </span>"
    subtitle_text: Who are our highest valued customers?
    body_text: "**Recommended Action** Explore from here to see what products a user\
      \ has purchased and include them in a targeted advertising campaign"
    row: 39
    col: 0
    width: 24
    height: 3
  filters:
  - name: Brand Name
    title: Brand Name
    type: field_filter
    default_value: Calvin Klein
    allow_multiple_values: true
    required: false
    model: thelook
    explore: order_items
    listens_to_filters: []
    field: products.brand
  - name: Date
    title: Date
    type: date_filter
    default_value: 90 days
    allow_multiple_values: true
    required: false
  - name: State
    title: State
    type: field_filter
    default_value: ''
    allow_multiple_values: true
    required: false
    model: thelook
    explore: order_items
    listens_to_filters: []
    field: users.state