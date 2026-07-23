from odoo import fields, models, api
from datetime import timedelta

class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_dead_line", inverse="_inverse_validity")


    @api.depends("validity")
    def _compute_dead_line(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_validity(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days
