with source as (

    select * from {{ ref('tvcamara_snapshot') }}

),

renamed as (

    select
        id::integer as tvcamara_id,
        title::varchar as tvcamara_title,
        url::varchar as tvcamara_url,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
