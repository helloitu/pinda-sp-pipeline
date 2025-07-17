with source as (

    select * from {{ ref('pautas_snapshot') }}

),

renamed as (

    select
        id::integer as pauta_id,
        name::varchar as pauta_name,
        date::date as pauta_date,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
