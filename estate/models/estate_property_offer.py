from datetime import date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, exceptions


class PropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offers"

    _sql_constraints = [
        ('check_positive_price', 'CHECK(price > 0)',
         'A property offer price must be strictly positive.')
    ]

    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    @api.model
    def create(self, vals):
        related_property = self.env['estate.property'].browse(vals['property_id'])
        for offer in related_property.offer_ids:
            if offer.price > self.price:
                raise exceptions.UserError("Higher offer already present")
        related_property.state = 'offer_received'
        return super().create(vals)

    def action_accept(self):
        related_offers_statuses = self.mapped("property_id.offer_ids.status")
        if any(x == 'accepted' for x in related_offers_statuses):
            raise exceptions.UserError("Another offer was already accepted")
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse(self):
        self.status = 'refused'
        return True

