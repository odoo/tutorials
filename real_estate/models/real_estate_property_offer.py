from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class real_estate_property_offer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Real Estate Property Offer'

    price = fields.Float(required=True)
    property_id = fields.Many2one('real.estate', string='Property', ondelete='cascade')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )
    _check_offer_price_positive = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date.date() + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Date.today() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date and offer.date_deadline:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_accept(self):
        # accepted_offer = self.search([
        #     ('property_id', '=', self.property_id.id),
        #     ('status', '=', 'accepted')
        # ], limit=1)
        # accepted_offer = self.property_id.offer_ids.filtered(
        #     lambda o: o.status == 'accepted'
        # )
        accepted_offer = self.property_id.offer_ids.filtered_domain([
            ('status', '=', 'accepted')
        ])
        if accepted_offer:
            raise UserError(
                "Only one offer can be accepted for a property."
            )
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.stage = 'sold'
        self.property_id.buyer_id = self.partner_id.id

    def action_refuse(self):
        self.status = 'refused'
