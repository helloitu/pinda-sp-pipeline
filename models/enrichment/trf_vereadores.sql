with source as (

    select * from {{ ref('vereadores_snapshot') }}

),

renamed as (

    select
        id::integer as vereador_id,
        name::varchar as vereador_name,
        party::varchar as party,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
