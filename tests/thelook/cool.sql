select
  q30.f15 as _2bt9s3ruiouwtsku9jzaip_date,
  q30.f14 as _2bt9s3ruiouwtsku9jzaip_market_cap,
  q30.f42 as _2irggci8k2cup9o8skk01f,
  q30.f22 as _58dixj6bnarn4ixohfkhv7,
  q30.f43 as _6kchincooc0mumxmxbflr6
from
  (
    select
      q11.f14 as f14,
      q11.f15 as f15,
      q11.f22 as f22,
      q20.f42 as f42,
      q20.f43 as f43
    from
      (
        select
          q9.f14 as f14,
          q9.f15 as f15,
          sum((q9.f20 - 5 :: float8)) as f22
        from
          (
            select
              q6.f14 as f14,
              q6.f15 as f15,
              avg(q6.f18) as f20
            from
              (
                select
                  bitcoin_prices.market_cap as f14,
                  date_trunc('year', bitcoin_prices._date :: timestamp_ltz) as f15,
                  date_trunc('month', bitcoin_prices._date :: timestamp_ltz) as f17,
                  (bitcoin_prices.high - bitcoin_prices.low) as f18,
                  bitcoin_prices._date :: timestamp_ltz as f8
                from
                  (
                    select
                      "DATE" as _date,
                      HIGH as high,
                      LOW as low,
                      "Market Cap" as market_cap
                    from
                      EXAMPLES.BITCOIN.BITCOIN_PRICES
                  ) bitcoin_prices
              ) q6
            where
              (
                (
                  (
                    '2014-06-02T17:01:51.464+00:00' :: timestamp_ltz <= q6.f8
                  )
                  and (
                    '2016-10-08T16:51:00.753+00:00' :: timestamp_ltz >= q6.f8
                  )
                )
                or (q6.f8 is null)
              )
            group by
              q6.f14,
              q6.f15,
              q6.f17
          ) q9
        group by
          q9.f14,
          q9.f15
      ) q11
      LEFT OUTER join (
        select
          q17.f36 as f36,
          q17.f37 as f37,
          avg(q17.f40) as f42,
          max(q17.f33) as f43
        from
          (
            select
              bitcoin_prices._date :: timestamp_ltz as f30,
              bitcoin_prices.low as f33,
              bitcoin_prices.market_cap as f36,
              date_trunc('year', bitcoin_prices._date :: timestamp_ltz) as f37,
              (bitcoin_prices.high - bitcoin_prices.low) as f40
            from
              (
                select
                  "DATE" as _date,
                  HIGH as high,
                  LOW as low,
                  "Market Cap" as market_cap
                from
                  EXAMPLES.BITCOIN.BITCOIN_PRICES
              ) bitcoin_prices
          ) q17
        where
          (
            (
              (
                '2014-06-02T17:01:51.464+00:00' :: timestamp_ltz <= q17.f30
              )
              and (
                '2016-10-08T16:51:00.753+00:00' :: timestamp_ltz >= q17.f30
              )
            )
            or (q17.f30 is null)
          )
        group by
          q17.f36,
          q17.f37
      ) q20 on (
        (
          (
            coalesce(
              q11.f15,
              '1970-01-01T00:00:00+00:00' :: timestamp_ltz
            ) = coalesce(
              q20.f37,
              '1970-01-01T00:00:00+00:00' :: timestamp_ltz
            )
          )
          and ((q11.f15 is not null) = (q20.f37 is not null))
        )
        and (
          (
            coalesce(q11.f14, 0 :: float8) = coalesce(q20.f36, 0 :: float8)
          )
          and ((q11.f14 is not null) = (q20.f36 is not null))
        )
      )
    order by
      q11.f14 asc,
      q11.f15 asc
    limit
      1001
  ) q30 -- Sigma Σ {"request-id":"a38ca919fbb84d0eb124ad6af3176e0c","email":"russelljgarner@gmail.com"}