view: cool {

dimension: foo {}
measure: bar {}
dimension_group: foo_date {}
filter: foo_filter {}
dimension: tst {}

dimension: hugo {

    link: {
      label: "Website"
      url: "http://www.google.com/search?q={{ value | encode_uri }}+clothes&btnI"
      icon_url: "http://www.google.com/s2/favicons?domain=www.{{ value | encode_uri }}.com"
    }

}

}
