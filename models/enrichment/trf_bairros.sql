with source as (

    select * from {{ ref('bairros_snapshot') }}

),

renamed as (

    select
        id::integer as bairro_id,
        name::varchar as bairro_name,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
