from datetime import datetime, timedelta

from odoo import api, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer'
    _sql_constraints = [
        ('check_price', 'CHECK (price > 0)', 'The price must be greater than 0'),
    ]

    price = fields.Float('Price', required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    create_date = fields.Date(string="Creation Date", default=lambda self: datetime.now())

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    validity = fields.Integer("Validity (days)")
    date_deadline = fields.Date("Deadline", readonly=False, compute="_compute_date_deadline")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = offer.create_date + timedelta(days=offer.validity)

    def _compute_date_deadline_inverse(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date).days

    def action_accepted(self):
        for offer in self:
            offer.property_id.sold(self)
            offer.status = 'accepted'

    def action_refused(self):
        for offer in self:
            offer.status = 'refused'
