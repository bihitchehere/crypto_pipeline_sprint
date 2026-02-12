{% macro filter_new_rows(table, column) %}
{% if is_incremental() %}
    {{ table }}.{{ column }} > (SELECT MAX({{ column }}) FROM {{ this }})
{% else %}
    1=1
{% endif %}
{% endmacro %}