WITH partner_company AS (
    SELECT
        rp.id AS partner_id,
        rp.partner_status_id,
        rp.phone,
        rp.city,
        rp.street,
        rp.capacity_tons
    FROM res_partner rp
    WHERE rp.active IS TRUE
      AND rp.is_company IS TRUE
),

partner_categ AS (
    SELECT
        rel.partner_id,
        rel.categ_id AS company_category_id
    FROM res_partner_product_category_rel rel
),

/* Build product -> category list from main + extra categories */
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

/* Match company category (and its children) to product categories */
matched_products AS (
    SELECT DISTINCT
        pc.partner_id,
        pc.company_category_id,
        pt.id AS product_tmpl_id,
        pt.name AS product_name,
        pt.dosage_per_ton AS dosage_per_ton
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
),

/* Fix: SOL product_id is product_product, map to template */
monthly_sales AS (
    SELECT
        so.partner_id,
        pp.product_tmpl_id,
        SUM(sol.product_uom_qty) AS monthly_qty
    FROM sale_order_line sol
    JOIN sale_order so ON so.id = sol.order_id
    JOIN product_product pp ON pp.id = sol.product_id
    WHERE so.state IN ('sale', 'done')
      AND so.date_order >= date_trunc('month', now())
      AND so.date_order < (date_trunc('month', now()) + interval '1 month')
    GROUP BY so.partner_id, pp.product_tmpl_id
),

last_salesperson AS (
    SELECT DISTINCT ON (so.partner_id, pp.product_tmpl_id)
        so.partner_id,
        pp.product_tmpl_id,
        so.user_id AS sales_manager_id
    FROM sale_order_line sol
    JOIN sale_order so ON so.id = sol.order_id
    JOIN product_product pp ON pp.id = sol.product_id
    WHERE so.state IN ('sale', 'done')
      AND so.date_order >= date_trunc('month', now())
      AND so.date_order < (date_trunc('month', now()) + interval '1 month')
    ORDER BY so.partner_id, pp.product_tmpl_id, so.date_order DESC, so.id DESC
)

SELECT
    row_number() OVER () AS id,

    pc.partner_id,
    pc.partner_status_id,
    pc.phone,
    pc.city,
    pc.street,
    pc.capacity_tons,

    mp.company_category_id,
    mp.product_tmpl_id,
    mp.product_name,
    COALESCE(mp.dosage_per_ton, 0.0) AS dosage_per_ton,

    (COALESCE(pc.capacity_tons, 0.0) * COALESCE(mp.dosage_per_ton, 0.0) / 1000.0) AS potential_monthly_demand,

    COALESCE(ms.monthly_qty, 0.0) AS monthly_result,

    (
      (COALESCE(pc.capacity_tons, 0.0) * COALESCE(mp.dosage_per_ton, 0.0) / 1000.0)
      - COALESCE(ms.monthly_qty, 0.0)
    ) AS difference_in_demand,

    lsp.sales_manager_id

FROM partner_company pc
JOIN matched_products mp
    ON mp.partner_id = pc.partner_id

LEFT JOIN monthly_sales ms
    ON ms.partner_id = pc.partner_id
   AND ms.product_tmpl_id = mp.product_tmpl_id

LEFT JOIN last_salesperson lsp
    ON lsp.partner_id = pc.partner_id
   AND lsp.product_tmpl_id = mp.product_tmpl_id
;
