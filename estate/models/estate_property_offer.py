from odoo import api, fields, models
from datetime import timedelta


class estatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Propert offers"

    price = fields.Float(string="Price")
    status = fields.Selection(
        copy="False",
        selection=[
            ("acctepted", "Acctepted"),
            ("refused", "Refused"),
        ],
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
        store=True,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = (offer.date_deadline - fields.Date.today()).days
