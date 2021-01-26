view: test1 {}
view: +test1 {
    sql_table_name: foo ;;
    dimension: first {}
}
view: +test1 {
    sql_table_name: bar ;;
    dimension: second {}
}