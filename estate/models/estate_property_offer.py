# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', "Accepted"), ('refused', "Refused")], copy=False)
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True, ondelete='cascade')
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
            if record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
                raise UserError(record.env_("Another offer has already been accepted."))
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env['estate.property'].browse(vals['property_id'])
            if float_compare(vals['price'], estate_property.best_offer, precision_digits=2) < 0:
                raise UserError(self.env._("The price must be higher than %s", estate_property.best_offer))

            estate_property.state = 'offer_received'

        return super().create(vals_list)
