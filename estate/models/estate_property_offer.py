from odoo import api, fields, models
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"

    price = fields.Float('Price', required=True)
    property_id = fields.Many2one('estate.property', 'property_id', required=True)
    partner_id = fields.Many2one('res.partner', required=True)
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ]
    )

    validity = fields.Integer(
        "Validity (days)",
        default=7,
        required=True,
    )
    date_deadline = fields.Date(
        "Deadline",
        required=True,
        compute="_compute_deadline",
        inverse="_inverse_deadline"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            delta = offer.date_deadline - fields.Date.today()
            offer.validity = delta.days