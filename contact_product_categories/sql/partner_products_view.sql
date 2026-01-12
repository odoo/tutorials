WITH partner_categ AS (
    SELECT
        rel.partner_id,
        rel.categ_id AS company_category_id
    FROM res_partner_product_category_rel rel
),

/* Product -> category list from main + extra categories */
product_all_categ AS (
    SELECT
        pt.id AS product_tmpl_id,
        pt.categ_id AS categ_id
    FROM product_template pt
    WHERE pt.active IS TRUE
      AND pt.categ_id IS NOT NULL

    UNION

    SELECT
        rel.product_tmpl_id AS product_tmpl_id,
        rel.categ_id AS categ_id
    FROM product_template_extra_category_rel rel
),

matched AS (
    SELECT DISTINCT
        pc.partner_id,
        pc.company_category_id,
        pt.id AS product_tmpl_id
    FROM partner_categ pc
    JOIN product_category company_cat
        ON company_cat.id = pc.company_category_id

    JOIN product_all_categ pac
        ON TRUE

    JOIN product_category prod_cat
        ON prod_cat.id = pac.categ_id

    JOIN product_template pt
        ON pt.id = pac.product_tmpl_id

    /* child-of using parent_path */
    WHERE prod_cat.parent_path LIKE company_cat.parent_path || '%%'
)

SELECT
    row_number() OVER () AS id,
    partner_id,
    company_category_id,
    product_tmpl_id
FROM matched;
