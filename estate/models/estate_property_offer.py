from datetime import datetime, timedelta

from odoo import api, fields, models, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer'
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK (price > 0)', 'The price must be greater than 0'),
    ]

    price = fields.Float("Price", required=True)
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    offer_date = fields.Date(string="Creation Date", default=lambda self: fields.Date.today())
    validity = fields.Integer("Validity (days)")

    date_deadline = fields.Date("Deadline", readonly=False, compute="_compute_date_deadline", inverse='_compute_date_deadline_inverse')

    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", related='property_id.property_type_id')

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.offer_date is not None:
                offer.date_deadline = fields.Date.to_date(offer.offer_date) + timedelta(days=offer.validity)

    def _compute_date_deadline_inverse(self):
        for offer in self:
            offer.validity = (fields.Date.to_date(offer.date_deadline) - fields.Date.to_date(offer.offer_date)).days

    def action_accepted(self):
        for offer in self:
            for prop_offer in offer.property_id.offer_ids:
                if prop_offer.status == 'accepted':
                    raise exceptions.UserError("Can't accept an offer when another offer has already been accepted for this property.")
            offer.property_id.mark_as_sold(self)
            offer.status = 'accepted'

    def action_refused(self):
        for offer in self:
            offer.status = 'refused'
