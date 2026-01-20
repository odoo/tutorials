from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class RealEstatePropertyOffer(models.Model):
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
        for val in vals:
            price = val.get('price')
            property_id = val.get('property_id')
            property = self.env['real.estate'].browse(property_id)
            if property.stage == "new":
                property.best_price = price
            elif float_compare(price, property.best_price, precision_rounding=0.01) < 0:
                raise UserError(
                    f"Price should be greater than {property.best_price}")
            else:
                property.best_price = price
            if property and property.stage == 'new':
                property.stage = 'offer_received'

        return super().create(vals)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + timedelta(days=offer.validity)

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
            'stage': 'offer_accepted',
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
