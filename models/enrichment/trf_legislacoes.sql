with source as (

    select * from {{ ref('legislacoes_snapshot') }}

),

renamed as (

    select
        id::integer as legislacao_id,
        name::varchar as legislacao_name,
        description::varchar as description,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
