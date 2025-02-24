# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from datetime import timedelta
from odoo import _
from odoo import api
from odoo import fields
from odoo import models
from odoo.exceptions import UserError

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        ('check_offer_price', "CHECK(price > 0)",
        "The offer price must be strictly positive"),
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False
    )
    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', string="Property Type", store=True, related='property_id.property_type_id')
    validity = fields.Integer(string="Validity (days)", default="7")
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = offer.create_date.date()
            else:
                create_date = fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            if offer.create_date:
                create_date = offer.create_date.date()
            else:
                create_date = fields.Date.today()
            offer.validity = (offer.date_deadline-create_date).days

    @api.model_create_multi
    def create(self, vals):
        for offer in vals:
            Property = self.env['estate.property'].browse(offer['property_id'])
            if Property.state=="sold":
                    raise UserError(_("Can't create an offer for sold property"))
            if Property.state != 'offer received':
                Property.state = 'offer received'
            existing_offers = Property.offer_ids.mapped('price')
            max_offer = max(existing_offers) if existing_offers else 0
            if Property.offer_ids and offer['price'] < max_offer:
                raise UserError(_("The offer must be higher than %f", Property.best_offer))
            return super().create(vals)

    def accept_offer(self):
        rc = self.property_id.offer_ids.mapped('status')
        if not any(status=='accepted' for status in rc):
            for offer in self:
                offer.property_id.selling_price=offer.price
                offer.status='accepted'
                offer.property_id.buyer_id=offer.partner_id
                offer.property_id.state='offer accepted'
        else:
            raise UserError(_("One of the offer is already accepted"))

    def refuse_offer(self):
        for offer in self:
            offer.status='refused'
