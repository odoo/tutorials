from odoo import fields, models, tools


def _addon_name():
    parts = __name__.split(".")
    # possible forms:
    # 1) contact_product_categories.models.market_view_report
    # 2) odoo.addons.contact_product_categories.models.market_view_report
    if len(parts) >= 3 and parts[0] == "odoo" and parts[1] == "addons":
        return parts[2]
    return parts[0]


MODULE = _addon_name()


class MarketViewReport(models.Model):
    _name = "market.view.report"
    _description = "Market View Report"
    _auto = False
    _rec_name = "partner_id"
    _order = "partner_id, company_category_id, product_tmpl_id"

    partner_id = fields.Many2one("res.partner", string="Client", readonly=True)
    partner_status_id = fields.Many2one("res.partner.status", string="Status", readonly=True)

    phone = fields.Char(string="Contact", readonly=True)
    city = fields.Char(string="City", readonly=True)
    street = fields.Char(string="Address", readonly=True)

    capacity_tons = fields.Float(string="Capacity (tons)", readonly=True)
    company_category_id = fields.Many2one("product.category", string="Business", readonly=True)

    product_tmpl_id = fields.Many2one("product.template", string="Product", readonly=True)
    product_name = fields.Char(string="Product Description", readonly=True)

    dosage_per_ton = fields.Float(string="Dosage (Kg/Ton)", readonly=True)
    potential_monthly_demand = fields.Float(string="Potential Monthly Demand", readonly=True)

    monthly_result = fields.Float(string="Monthly Result", readonly=True)
    difference_in_demand = fields.Float(string="Difference in Demand", readonly=True)

    sales_manager_id = fields.Many2one("res.users", string="Sales Manager", readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)

        rel_path = f"{MODULE}/sql/market_view_report.sql"

        try:
            with tools.file_open(rel_path, "rb") as f:
                view_body = f.read().decode("utf-8").strip().rstrip(";")
        except FileNotFoundError:
            raise FileNotFoundError(f"SQL file not found: {rel_path}")

        self.env.cr.execute(f"CREATE OR REPLACE VIEW {self._table} AS ({view_body})")
