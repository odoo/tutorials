from odoo import api, fields, models


class MarketViewReportRun(models.Model):
    _name = "market.view.report.run"
    _description = "Market View Report Run"
    _order = "create_date desc"

    name = fields.Char(required=True, default="Market View Run")
    user_id = fields.Many2one("res.users", required=True, default=lambda self: self.env.user)
    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    include_opportunities = fields.Boolean(default=False)

    line_ids = fields.One2many("market.view.report.run.line", "run_id", readonly=True)


class MarketViewReportRunLine(models.Model):
    _name = "market.view.report.run.line"
    _description = "Market View Report Run Line"
    _order = "partner_id, company_category_id, product_tmpl_id"

    run_id = fields.Many2one("market.view.report.run", required=True, ondelete="cascade")

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

    # period anchors for pivoting
    period_day = fields.Date(string="Day", readonly=True)
    period_month = fields.Date(string="Month", readonly=True)
    period_week = fields.Date(string="Week", readonly=True)
    period_year = fields.Date(string="Year", readonly=True)

    is_opportunity = fields.Boolean(string="Opportunity", readonly=True, default=False)

    @api.depends("run_id")
    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.partner_id.display_name} / {rec.product_tmpl_id.display_name}"
