import datetime

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CoationsClaims(models.Model):
    _name = "coatations.claims"
    _description = "List of all coations"
    name = fields.Char(
        string="Order Reference",
        required=True,
        copy=False,
        readonly=True,
        index="trigram",
        default=lambda self: ("New"),
    )
    partner_id = fields.Many2one("res.partner")
    client_id = fields.Many2one("res.partner")
    reseller_id = fields.Many2one("res.partner", string="Reseller", readonly=False)
    date_from = fields.Date(default=lambda self: fields.Datetime.today(),required=True)
    date_to = fields.Date()
    state = fields.Selection(
        string="state",
        selection=[("new", "New"), ("active", "Active"), ("expired", "Expired")],
        default="new",
    )
    coation_lines_ids = fields.One2many("coatations.lines", "coation_id")
    sale_order_ids = fields.Many2many("sale.order")
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                year = datetime.datetime.now().year
                sequence = self.env["ir.sequence"].next_by_code(self.id) or "0000"
                vals["name"] = f"COT/{year}/{sequence}"

        return super(CoationsClaims, self).create(vals)

    @api.constrains("date_from", "date_to")
    def _check_date_range(self):
        for record in self:
            if record.date_from and record.date_to:
                if record.date_to < record.date_from:
                    raise ValidationError(
                        "The 'Date To' cannot be earlier than 'Date From'. Please correct the dates."
                    )
