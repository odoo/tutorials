from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError


class real_estate_property_offer(models.Model):
    _name = 'real.estate.property.offer'
    _description = 'Real Estate Property Offer'
    _order = "price desc"

    price = fields.Float(required=True)
    property_id = fields.Many2one('real.estate', string='Property', ondelete='restrict')
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )
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

    @api.model
    def create(self, vals):
        # property_id = vals.get('property_id')
        # price = vals.get('price')
        # if property_id and price:
        #     property_rec = self.env['estate.property'].browse(property_id)
        #     if property_rec.offer_ids:
        #         max_offer = max(property_rec.offer_ids.mapped('price'))
        #         if price < max_offer:
        #             raise UserError(
        #                 "The offer must be higher than existing offers."
        #             )
        offer = super().create(vals)
        if offer.property_id and offer.property_id.stage == 'new':
            offer.property_id.stage = 'offer_received'
        return offer

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

    @api.ondelete(at_uninstall=False)
    def _unlink_if_accepted_offer(self):
        accepted_offer = self.filtered_domain([('status', '=', 'accepted')])
        if accepted_offer:
            raise UserError("Can't delete an active record!")

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
        maintenace_request = self.property_id.maintenance_request_ids.filtered_domain([('status', '!=', 'done')])
        if accepted_offer:
            raise UserError(
                "Only one offer can be accepted for a property.")
        if maintenace_request:
            raise UserError("Property cannot be sold , there is any maintenance request not done")
        self.status = 'accepted'
        self.property_id.write({
            'selling_price': self.price,
            'stage': 'sold',
            'buyer_id': self.partner_id.id,
        })
        refused_offer = self.property_id.offer_ids.filtered_domain([
            ('id', '!=', 'self.id'),
            ('status', '!=', 'accepted')
        ])
        for refuse in refused_offer:
            refuse.status = 'refused'

    def action_refuse(self):
        self.status = 'refused'
