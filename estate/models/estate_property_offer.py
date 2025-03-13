# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', "Offer price must be strictly positive!"),
    ]

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused")
        ],
        string="Status", copy=False
    )
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(comodel_name='estate.property.type', related='property_id.property_type_id', string="Property Type")
    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)
            else:
                offer.date_deadline = fields.Date.add(fields.Date.today(), days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.to_date(offer.create_date)).days

    def action_accept_offer(self):
        for offer in self:
            if 'accepted' not in offer.property_id.offer_ids.mapped('status'):
                offer.status = 'accepted'
                offer.property_id.state = 'offer_accepted'
                offer.property_id.selling_price = offer.price
                offer.property_id.partner_id = offer.partner_id
            else:
                raise UserError("This property already has an accepted offer.")

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env['estate.property'].browse(offer.get('property_id'))
            if property.state == 'sold':
                raise UserError("Property is already sold.")
            if property.best_price > offer.get('price'):
                raise UserError("Offer price can't be less than the current best offer.")
            property.state = 'offer_received'
        return super().create(vals_list)
