with payments as (
    select * from public.freshnes_test
),
final as (
    select
        *
    from payments
)
select * from final