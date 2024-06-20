# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError

class PropertyOffer(models.Model):
    _name = "property.offer"
    _description = "Property offers for the Real Estate"
    _order = "price"

    price = fields.Float()
    status = fields.Selection(copy = False, selection=[
        ('accepted','Accepted'),
        ('refused','Refused')])
    partner_id = fields.Many2one("res.partner", required = True)
    property_id = fields.Many2one("property", required = True)
    validity = fields.Integer(default = 7) # must be in days
    create_date = fields.Date(default = fields.Datetime.today())
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')
    property_type_id = fields.Many2one("property.type", string="Property Type", related = "property_id.property_type_id")

    _sql_constraints  = [
        ('check_offer_price', 'CHECK(price > 0)', 'Odoopsie! The offer price must be positive' )
    ]

    @api.depends('validity')
    def _compute_date_deadline(self) :
        for offer in self :
            offer.date_deadline = offer.create_date + relativedelta(days = offer.validity)

    def _inverse_date_deadline(self) :
        for offer in self :
            offer.validity = (offer.date_deadline - offer.create_date).days

    def action_set_offer_accepted(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = 'offer_accepted'
        return True

    def action_set_offer_refused(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model
    def create(self, vals_list):
        targeted_property = self.env['property'].browse(vals_list['property_id'])
        if targeted_property.state == 'new' : targeted_property.state = 'offer_received'
        for offer in targeted_property.offer_ids :
            if vals_list['price'] < offer.price : raise UserError("Odoopsie! There is already a better offer for this property.")
        return super().create(vals_list)