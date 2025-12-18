from odoo import models, fields, api
from datetime import timedelta


class offers_model(models.Model):
    _name = "estate.offers"
    _description = "Offers Model"

    price = fields.Integer(required=True)
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        required=True,
    )
    building_id = fields.Many2one("estate.buildings", string="Building")
    partner_id = fields.Many2one("res.partner", string="Partner")
    validity = fields.Integer(
        string="Validity (days)", default=7
    )
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
    
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days
