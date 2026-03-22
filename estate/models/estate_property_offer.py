# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    _check_offer_price = models.Constraint('CHECK(price > 0)', "The offer price must be stricly positive")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(starting_date, days=record.validity)

    @api.depends('create_date', 'validity')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            for offer in record.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise UserError(self.env_("Another offer has already been accepted."))
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True
