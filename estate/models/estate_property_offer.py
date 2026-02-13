from datetime import timedelta
from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer model"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("rejected", "Rejected")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Date Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for rec in self:
            curr_date = rec.create_date
            rec.date_deadline = (
                (curr_date + timedelta(days=rec.validity))
                if curr_date
                else fields.Date.today() + timedelta(days=rec.validity)
            )

    @api.onchange("date_deadline")
    def _inverse_deadline(self):
        for rec in self:
            start_date = (
                rec.create_date.date() if rec.create_date else fields.Date.today()
            )
            rec.validity = (rec.date_deadline - start_date).days
