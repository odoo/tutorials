import datetime
from odoo import api, fields, models


class HrTdsDeclaration(models.Model):
    _name = "hr.tds.declaration"
    _description = "TDS declaration"

    def _get_financial_year_selection(self):
        current_year = datetime.date.today().year
        previous_year = f"{current_year - 1} - {current_year}"
        current_financial_year = f"{current_year} - {current_year + 1}"
        return [(previous_year, previous_year), (current_financial_year, current_financial_year)]

    name = fields.Char(string="TDS Declaration", required=True)
    tds_declaration_ids = fields.One2many("hr.tds.declaration.details", "tds_declaration_id")
    financial_year = fields.Selection(
        selection=_get_financial_year_selection,
        string="Financial Year",
        required=True,
        default=lambda self: f"{datetime.date.today().year}-{datetime.date.today().year + 1}",
        )
    start_date = fields.Date(string="Start Date", compute="_compute_dates", readonly=False)
    end_date = fields.Date(string="End Date", compute="_compute_dates", readonly=False)
    tds_declaration_count = fields.Integer(compute="_compute_declarations_count")
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("accepted", "Accepted")
        ],
        string="Status",
        default="new"
    )

    @api.depends("financial_year")
    def _compute_dates(self):
        for financial_year_record in self:
            start_year = int(financial_year_record.financial_year.split("-")[0])
            end_year = int(financial_year_record.financial_year.split("-")[1])
            financial_year_record.start_date = fields.Date.to_date(f"{start_year}-04-01")
            financial_year_record.end_date = fields.Date.to_date(f"{end_year}-03-31")

    def _compute_declarations_count(self):
        self.tds_declaration_count = len(self.tds_declaration_ids)

    def action_approved(self):
        self.ensure_one()
        self.state = "accepted"

    def action_set_to_draft(self):
        self.ensure_one()
        self.state = "draft"

    def action_open_declarations(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "hr.tds.declaration.details",
            "views": [[False, "list"], [False, "form"]],
            "domain": [["id", "in", self.tds_declaration_ids.ids]],
            "name": f"TDS Declaration {self.financial_year}",
        }
