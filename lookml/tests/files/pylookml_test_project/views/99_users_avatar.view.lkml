include: "/views/**/01_order_items.view.lkml"
include: "/views/**/02_users.view.lkml"
## kittens for certain demos

view: kitten_users {
  extends: [users]

  dimension: portrait {
    label: "Kitten Portrait"
    sql: GREATEST(MOD(${id}*97,867),MOD(${id}*31,881),MOD(${id}*72,893)) ;;
    type: number
    html: <img height=80 width=80 src="http://placekitten.com/g/{{ value }}/{{ value }}">
      ;;
  }

  dimension: name {
    label: "Kitten Name"
    sql: CONCAT(${first_name},' ',${TABLE}.last_name) ;;
  }

  dimension: first_name {
    label: "Kitten First Name"

    case: {
      when: {
        sql: MOD(${id},24) = 23 ;;
        label: "Bella"
      }

      when: {
        sql: MOD(${id},24) = 22 ;;
        label: "Bandit"
      }

      when: {
        sql: MOD(${id},24) = 21 ;;
        label: "Tigger"
      }

      when: {
        sql: MOD(${id},24) = 20 ;;
        label: "Boots"
      }

      when: {
        sql: MOD(${id},24) = 19 ;;
        label: "Chloe"
      }

      when: {
        sql: MOD(${id},24) = 18 ;;
        label: "Maggie"
      }

      when: {
        sql: MOD(${id},24) = 17 ;;
        label: "Pumpkin"
      }

      when: {
        sql: MOD(${id},24) = 16 ;;
        label: "Oliver"
      }

      when: {
        sql: MOD(${id},24) = 15 ;;
        label: "Sammy"
      }

      when: {
        sql: MOD(${id},24) = 14 ;;
        label: "Shadow"
      }

      when: {
        sql: MOD(${id},24) = 13 ;;
        label: "Sassy"
      }

      when: {
        sql: MOD(${id},24) = 12 ;;
        label: "Kitty"
      }

      when: {
        sql: MOD(${id},24) = 11 ;;
        label: "Snowball"
      }

      when: {
        sql: MOD(${id},24) = 10 ;;
        label: "Snickers"
      }

      when: {
        sql: MOD(${id},24) = 9 ;;
        label: "Socks"
      }

      when: {
        sql: MOD(${id},24) = 8 ;;
        label: "Gizmo"
      }

      when: {
        sql: MOD(${id},24) = 7 ;;
        label: "Jake"
      }

      when: {
        sql: MOD(${id},24) = 6 ;;
        label: "Lily"
      }

      when: {
        sql: MOD(${id},24) = 5 ;;
        label: "Charlie"
      }

      when: {
        sql: MOD(${id},24) = 4 ;;
        label: "Peanut"
      }

      when: {
        sql: MOD(${id},24) = 3 ;;
        label: "Zoe"
      }

      when: {
        sql: MOD(${id},24) = 2 ;;
        label: "Felix"
      }

      when: {
        sql: MOD(${id},24) = 1 ;;
        label: "Mimi"
      }

      when: {
        sql: MOD(${id},24) = 0 ;;
        label: "Jasmine"
      }
    }
  }

#   set: detail {
#     fields: [EXTENDED*, portrait]
#   }
}

view: kitten_order_items {
  extends: [order_items]

#   set: detail {
#     fields: [EXTENDED*, users.portrait]
#   }
}
