from datetime import date, timedelta

from odoo import api, fields, models


class MarketViewReportWizard(models.TransientModel):
    _name = "market.view.report.wizard"
    _description = "Market View Report Wizard"

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    include_opportunities = fields.Boolean(string="Include opportunities (zero sales in range)", default=False)

    preset = fields.Selection(
        [
            ("current_month", "Current Month"),
            ("last_month", "Last Month"),
            ("last_3_months", "Last 3 Months"),
            ("custom", "Custom"),
        ],
        default="current_month",
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        today = fields.Date.context_today(self)
        first_this_month = today.replace(day=1)
        # end of month = first of next month - 1 day
        this_month_end = (first_this_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        res.setdefault("preset", "current_month")
        res.setdefault("date_from", first_this_month)
        res.setdefault("date_to", this_month_end)
        return res

    @api.onchange("preset")
    def _onchange_preset(self):
        today = fields.Date.context_today(self)
        first_this_month = today.replace(day=1)

        if self.preset == "current_month":
            this_month_end = (first_this_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            self.date_from = first_this_month
            self.date_to = this_month_end

        elif self.preset == "last_month":
            last_month_end = first_this_month - timedelta(days=1)
            self.date_to = last_month_end
            self.date_from = last_month_end.replace(day=1)

        elif self.preset == "last_3_months":
            last_month_end = first_this_month - timedelta(days=1)
            m = last_month_end.month
            y = last_month_end.year
            for _ in range(2):
                m -= 1
                if m == 0:
                    m = 12
                    y -= 1
            self.date_from = date(y, m, 1)
            self.date_to = last_month_end

    def action_open_report(self):
        self.ensure_one()

        # Create run header
        run = self.env["market.view.report.run"].create(
            {
                "name": f"Market View {self.date_from}..{self.date_to}",
                "user_id": self.env.user.id,
                "date_from": self.date_from,
                "date_to": self.date_to,
                "include_opportunities": self.include_opportunities,
            }
        )

        # Optional: cleanup old runs for the same user (keep last 10)
        old_runs = self.env["market.view.report.run"].search(
            [("user_id", "=", self.env.user.id), ("id", "!=", run.id)], order="create_date desc", offset=10
        )
        if old_runs:
            old_runs.unlink()

        # Generate lines with SQL (fast + correct for pivot)
        cr = self.env.cr

        # 1) Insert SALES rows aggregated in selected range
        sales_insert_sql = """
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
            SELECT rel.partner_id, rel.categ_id AS company_category_id
            FROM res_partner_product_category_rel rel
        ),

        product_all_categ AS (
            SELECT pt.id AS product_tmpl_id, pt.categ_id AS categ_id
            FROM product_template pt
            WHERE pt.active IS TRUE AND pt.categ_id IS NOT NULL
            UNION
            SELECT rel.product_tmpl_id AS product_tmpl_id, rel.categ_id AS categ_id
            FROM product_template_extra_category_rel rel
        ),

        matched_products AS (
            SELECT DISTINCT
                pc.partner_id,
                pc.company_category_id,
                pt.id AS product_tmpl_id,
                pt.name AS product_name,
                pt.dosage_per_ton AS dosage_per_ton
            FROM partner_categ pc
            JOIN product_category company_cat ON company_cat.id = pc.company_category_id
            JOIN product_all_categ pac ON TRUE
            JOIN product_category prod_cat ON prod_cat.id = pac.categ_id
            JOIN product_template pt ON pt.id = pac.product_tmpl_id
            WHERE prod_cat.parent_path LIKE company_cat.parent_path || '%%'
        ),

        sales_fact AS (
            SELECT
                so.partner_id,
                so.user_id AS sales_manager_id,
                pp.product_tmpl_id,
                so.date_order::date AS period_day,
                SUM(sol.product_uom_qty) AS sold_qty
            FROM sale_order_line sol
            JOIN sale_order so ON so.id = sol.order_id
            JOIN product_product pp ON pp.id = sol.product_id
            WHERE so.state IN ('sale','done')
              AND so.date_order::date >= %(date_from)s
              AND so.date_order::date <= %(date_to)s
            GROUP BY so.partner_id, so.user_id, pp.product_tmpl_id, so.date_order::date
        )

        INSERT INTO market_view_report_run_line (
            run_id,
            partner_id, partner_status_id, phone, city, street, capacity_tons,
            company_category_id,
            product_tmpl_id, product_name,
            dosage_per_ton, potential_monthly_demand,
            monthly_result, difference_in_demand,
            sales_manager_id,
            period_day, period_month, period_week, period_year,
            is_opportunity
        )
        SELECT
            %(run_id)s AS run_id,

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

            COALESCE(sf.sold_qty, 0.0) AS monthly_result,
            (COALESCE(sf.sold_qty, 0.0) - (COALESCE(pc.capacity_tons, 0.0) * COALESCE(mp.dosage_per_ton, 0.0) / 1000.0)) AS difference_in_demand,

            sf.sales_manager_id,

            sf.period_day,
            date_trunc('month', sf.period_day)::date AS period_month,
            date_trunc('week',  sf.period_day)::date AS period_week,
            date_trunc('year',  sf.period_day)::date AS period_year,

            FALSE AS is_opportunity

        FROM sales_fact sf
        JOIN partner_company pc
            ON pc.partner_id = sf.partner_id
        JOIN matched_products mp
            ON mp.partner_id = sf.partner_id
           AND mp.product_tmpl_id = sf.product_tmpl_id
        ;
        """

        cr.execute(
            sales_insert_sql,
            {"run_id": run.id, "date_from": self.date_from, "date_to": self.date_to},
        )

        # 2) Insert OPPORTUNITY rows only if toggle enabled:
        #    "zero sales in selected range" => NOT EXISTS sale_order_line in range for partner+product
        if self.include_opportunities:
            opportunities_insert_sql = """
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
                SELECT rel.partner_id, rel.categ_id AS company_category_id
                FROM res_partner_product_category_rel rel
            ),

            product_all_categ AS (
                SELECT pt.id AS product_tmpl_id, pt.categ_id AS categ_id
                FROM product_template pt
                WHERE pt.active IS TRUE AND pt.categ_id IS NOT NULL
                UNION
                SELECT rel.product_tmpl_id AS product_tmpl_id, rel.categ_id AS categ_id
                FROM product_template_extra_category_rel rel
            ),

            matched_products AS (
                SELECT DISTINCT
                    pc.partner_id,
                    pc.company_category_id,
                    pt.id AS product_tmpl_id,
                    pt.name AS product_name,
                    pt.dosage_per_ton AS dosage_per_ton
                FROM partner_categ pc
                JOIN product_category company_cat ON company_cat.id = pc.company_category_id
                JOIN product_all_categ pac ON TRUE
                JOIN product_category prod_cat ON prod_cat.id = pac.categ_id
                JOIN product_template pt ON pt.id = pac.product_tmpl_id
                WHERE prod_cat.parent_path LIKE company_cat.parent_path || '%%'
            )

            INSERT INTO market_view_report_run_line (
                run_id,
                partner_id, partner_status_id, phone, city, street, capacity_tons,
                company_category_id,
                product_tmpl_id, product_name,
                dosage_per_ton, potential_monthly_demand,
                monthly_result, difference_in_demand,
                sales_manager_id,
                period_day, period_month, period_week, period_year,
                is_opportunity
            )
            SELECT
                %(run_id)s AS run_id,

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

                0.0 AS monthly_result,
                (COALESCE(pc.capacity_tons, 0.0) * COALESCE(mp.dosage_per_ton, 0.0) / 1000.0) AS difference_in_demand,

                NULL::integer AS sales_manager_id,

                %(date_to)s::date AS period_day,
                date_trunc('month', %(date_to)s::date)::date AS period_month,
                date_trunc('week',  %(date_to)s::date)::date AS period_week,
                date_trunc('year',  %(date_to)s::date)::date AS period_year,

                TRUE AS is_opportunity

            FROM matched_products mp
            JOIN partner_company pc
                ON pc.partner_id = mp.partner_id

            WHERE NOT EXISTS (
                SELECT 1
                FROM sale_order_line sol
                JOIN sale_order so ON so.id = sol.order_id
                JOIN product_product pp ON pp.id = sol.product_id
                WHERE so.state IN ('sale','done')
                  AND so.partner_id = mp.partner_id
                  AND pp.product_tmpl_id = mp.product_tmpl_id
                  AND so.date_order::date >= %(date_from)s
                  AND so.date_order::date <= %(date_to)s
            );
            """

            cr.execute(
                opportunities_insert_sql,
                {"run_id": run.id, "date_from": self.date_from, "date_to": self.date_to},
            )

        # Open run lines in list/pivot/graph
        action = self.env.ref("contact_product_categories.action_market_view_report_run_lines").read()[0]
        action["domain"] = [("run_id", "=", run.id)]
        action["context"] = {"search_default_group_month": 1}
        return action


