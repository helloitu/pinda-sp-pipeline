with source as (

    select * from {{ ref('proposicoes_snapshot') }}

),

renamed as (

    select
        id::integer as proposicao_id,
        name::varchar as proposicao_name,
        description::varchar as description,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
