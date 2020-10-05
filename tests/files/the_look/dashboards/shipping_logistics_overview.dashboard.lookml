- dashboard: shipping_logistics__operations_overview
  title: Shipping Logistics & Operations Overview
  layout: newspaper
  description: 'Shipping and logistics overview for an ecommerce store - showing things like how many orders are processing, and where things are shipping'
  embed_style:
    background_color: ''
    show_title: true
    title_color: "#3a4245"
    show_filters_bar: true
    tile_text_color: "#3a4245"
    text_tile_text_color: ''
  elements:
  - title: Order Shipment Status
    name: Order Shipment Status
    model: thelook
    explore: order_items
    type: looker_column
    fields: [order_items.created_date, order_items.status, order_items.order_count]
    pivots: [order_items.status]
    filters:
      order_items.created_date: 60 days
      order_items.status: Complete,Shipped,Processing
    sorts: [order_items.created_date desc, order_items.status]
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: false
    color_palette: Custom
    limit_displayed_rows: false
    stacking: normal
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
    show_x_axis_label: false
    show_x_axis_ticks: true
    x_axis_scale: auto
    ordering: none
    show_null_labels: false
    colors: [green, red, orange]
    y_axis_scale_mode: linear
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    hidden_fields: []
    y_axes: []
    listen:
      Distribution Center: distribution_centers.name
    row: 5
    col: 0
    width: 16
    height: 8
  - title: Open Orders >3 Days Old
    name: Open Orders >3 Days Old
    model: thelook
    explore: order_items
    type: looker_grid
    fields: [order_items.order_id, users.email, order_items.created_date, order_items.status,
      products.item_name, order_items.days_to_process]
    filters:
      order_items.created_date: before 3 days ago
      order_items.status: Processing
    sorts: [order_items.days_to_process desc]
    limit: 25
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: false
    show_row_numbers: true
    transpose: false
    truncate_text: true
    hide_totals: false
    hide_row_totals: false
    size_to_fit: true
    series_cell_visualizations:
      order_items.days_to_process:
        is_active: false
        palette:
          palette_id: 90a81bec-f33f-43c9-a36a-0ea5f037dfa0
          collection_id: f14810d2-98d7-42df-82d0-bc185a074e42
    table_theme: transparent
    limit_displayed_rows: false
    enable_conditional_formatting: true
    header_text_alignment: left
    header_font_size: '12'
    rows_font_size: '12'
    conditional_formatting: [{type: along a scale..., value: !!null '', background_color: "#2196F3",
        font_color: !!null '', color_application: {collection_id: f14810d2-98d7-42df-82d0-bc185a074e42,
          palette_id: 90a81bec-f33f-43c9-a36a-0ea5f037dfa0, options: {steps: 5, reverse: true}},
        bold: false, italic: false, strikethrough: false, fields: [order_items.days_to_process]}]
    conditional_formatting_include_totals: false
    conditional_formatting_include_nulls: false
    truncate_column_names: false
    hidden_fields: []
    y_axes: []
    series_types: {}
    listen:
      Distribution Center: distribution_centers.name
    row: 17
    col: 0
    width: 24
    height: 8
  - title: Open Orders - Where do we need to ship?
    name: Open Orders - Where do we need to ship?
    model: thelook
    explore: order_items
    type: looker_map
    fields: [distribution_centers.location, users.approx_location, order_items.average_days_to_process]
    filters:
      order_items.status: '"Processing"'
      order_items.order_count: ">0"
    sorts: [order_items.average_days_to_process desc]
    limit: 500
    map_plot_mode: lines
    heatmap_gridlines: true
    map_tile_provider: positron
    map_position: custom
    map_scale_indicator: 'off'
    map_pannable: true
    map_zoomable: true
    map_marker_type: circle
    map_marker_icon_name: default
    map_marker_radius_mode: proportional_value
    map_marker_units: meters
    map_marker_proportional_scale_type: linear
    map_marker_color_mode: fixed
    show_view_names: true
    show_legend: true
    quantize_map_value_colors: false
    map_latitude: 36.31512514748051
    map_longitude: -92.10937499999999
    map_zoom: 3
    hidden_fields: []
    y_axes: []
    listen:
      Distribution Center: distribution_centers.name
    row: 35
    col: 0
    width: 13
    height: 8
  - title: Average Shipping Time to Users
    name: Average Shipping Time to Users
    model: thelook
    explore: order_items
    type: looker_map
    fields: [users.approx_location, order_items.average_shipping_time]
    filters:
      users.approx_location_bin_level: '7'
    sorts: [order_items.average_shipping_time desc]
    limit: 5000
    map_plot_mode: automagic_heatmap
    heatmap_gridlines: true
    map_tile_provider: positron
    map_position: custom
    map_scale_indicator: 'off'
    map_pannable: true
    map_zoomable: true
    map_marker_type: circle
    map_marker_icon_name: default
    map_marker_radius_mode: proportional_value
    map_marker_units: meters
    map_marker_proportional_scale_type: linear
    map_marker_color_mode: fixed
    show_view_names: true
    show_legend: true
    quantize_map_value_colors: false
    map_latitude: 36.527294814546245
    map_longitude: -92.19726562500001
    map_zoom: 3
    hidden_fields: []
    y_axes: []
    listen:
      Distribution Center: distribution_centers.name
    row: 27
    col: 13
    width: 11
    height: 16
  - title: Most Common Shipping Locations
    name: Most Common Shipping Locations
    model: thelook
    explore: order_items
    type: looker_map
    fields: [distribution_centers.location, users.approx_location, order_items.order_count]
    filters:
      order_items.order_count: ">30"
    sorts: [order_items.created_date, order_items.order_id, order_items.order_count
        desc]
    limit: 1000
    map_plot_mode: lines
    heatmap_gridlines: true
    map_tile_provider: positron
    map_position: custom
    map_scale_indicator: 'off'
    map_pannable: true
    map_zoomable: true
    map_marker_type: circle
    map_marker_icon_name: default
    map_marker_radius_mode: proportional_value
    map_marker_units: meters
    map_marker_proportional_scale_type: linear
    map_marker_color_mode: fixed
    show_view_names: true
    show_legend: true
    quantize_map_value_colors: false
    map_latitude: 43.58039085560786
    map_longitude: -61.52343749999999
    map_zoom: 3
    map_value_scale_clamp_max: 300
    map_value_scale_clamp_min: 30
    hidden_fields: []
    y_axes: []
    listen:
      Distribution Center: distribution_centers.name
    row: 27
    col: 0
    width: 13
    height: 8
  - title: Inventory Aging Report
    name: Inventory Aging Report
    model: thelook
    explore: order_items
    type: looker_column
    fields: [inventory_items.days_in_inventory_tier, inventory_items.count]
    filters:
      inventory_items.is_sold: 'No'
    sorts: [inventory_items.days_in_inventory_tier]
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    stacking: normal
    show_value_labels: true
    label_density: 25
    legend_position: center
    x_axis_gridlines: false
    y_axis_gridlines: true
    show_view_names: false
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
    colors: [grey]
    limit_displayed_rows: false
    y_axis_scale_mode: linear
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    series_colors: {}
    hidden_fields: []
    y_axes: []
    note_state: collapsed
    note_display: below
    note_text: Unsold inventory only
    listen:
      Distribution Center: distribution_centers.name
    row: 2
    col: 16
    width: 8
    height: 11
  - title: "# Orders Processing"
    name: "# Orders Processing"
    model: thelook
    explore: order_items
    type: single_value
    fields: [order_items.order_count]
    filters:
      order_items.status: Processing
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: false
    color_palette: Custom
    limit_displayed_rows: false
    stacking: normal
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
    show_x_axis_label: false
    show_x_axis_ticks: true
    x_axis_scale: auto
    ordering: none
    show_null_labels: false
    colors: [green, red, orange]
    y_axis_scale_mode: linear
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    hidden_fields: []
    y_axes: []
    series_types: {}
    row: 2
    col: 0
    width: 6
    height: 3
  - title: "# Orders Shipped"
    name: "# Orders Shipped"
    model: thelook
    explore: order_items
    type: single_value
    fields: [order_items.order_count]
    filters:
      order_items.status: Shipped
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: false
    color_palette: Custom
    limit_displayed_rows: false
    stacking: normal
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
    show_x_axis_label: false
    show_x_axis_ticks: true
    x_axis_scale: auto
    ordering: none
    show_null_labels: false
    colors: [green, red, orange]
    y_axis_scale_mode: linear
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    hidden_fields: []
    y_axes: []
    series_types: {}
    row: 2
    col: 11
    width: 5
    height: 3
  - title: Total Amount Processing
    name: Total Amount Processing
    model: thelook
    explore: order_items
    type: single_value
    fields: [order_items.total_sale_price]
    filters:
      order_items.status: Processing
    limit: 500
    column_limit: 50
    query_timezone: America/Los_Angeles
    show_view_names: false
    color_palette: Custom
    limit_displayed_rows: false
    stacking: normal
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
    show_x_axis_label: false
    show_x_axis_ticks: true
    x_axis_scale: auto
    ordering: none
    show_null_labels: false
    colors: [green, red, orange]
    y_axis_scale_mode: linear
    show_totals_labels: false
    show_silhouette: false
    totals_color: "#808080"
    hidden_fields: []
    y_axes: []
    series_types: {}
    row: 2
    col: 6
    width: 5
    height: 3
  - name: "<span class='fa fa-tachometer'> Operations Overview</span>"
    type: text
    title_text: "<span class='fa fa-tachometer'> Operations Overview</span>"
    subtitle_text: How are we doing from a logistics standpoint?
    body_text: ''
    row: 0
    col: 0
    width: 24
    height: 2
  - name: "<span class='fa fa-bell-o'> Orders Still Processing</span>"
    type: text
    title_text: "<span class='fa fa-bell-o'> Orders Still Processing</span>"
    subtitle_text: What orders should have been shipped but are still processing?
    body_text: "**Recommended Action** Send order id over slack to follow up on the\
      \ order status, then email the customer to let them know that there is a delay"
    row: 13
    col: 0
    width: 24
    height: 4
  - name: "<span class='fa fa-paper-plane'> Shipping by Location</span>"
    type: text
    title_text: "<span class='fa fa-paper-plane'> Shipping by Location</span>"
    subtitle_text: Where can we improve our shipping time?
    row: 25
    col: 0
    width: 24
    height: 2
  filters:
  - name: Distribution Center
    title: Distribution Center
    type: field_filter
    default_value: ''
    allow_multiple_values: false
    required: false
    model: thelook
    explore: order_items
    listens_to_filters: []
    field: distribution_centers.name
