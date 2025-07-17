with source as (

    select * from {{ ref('noticias_snapshot') }}

),

renamed as (

    select
        id::integer as noticia_id,
        title::varchar as noticia_title,
        content::varchar as noticia_content,
        dbt_updated_at,
        dbt_valid_from,
        dbt_valid_to
    from source

)

select * from renamed
