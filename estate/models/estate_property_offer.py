# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, exceptions
from datetime import date, timedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"

    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', copy=False,
                            selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', related="property_id.property_type_id", store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive',
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if record.create_date else date.today()) + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - (record.create_date.date() if record.create_date else date.today())).days

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if 'property_id' in vals and vals.get('property_id'):
                current_property = self.env['estate.property'].browse(vals['property_id'])
                if 'price' in vals and current_property.best_offer > vals.get('price', 0):
                    raise exceptions.ValidationError(f'The offer must be higher than {current_property.best_offer}')
                if current_property.state == 'new':
                    current_property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        self.ensure_one()
        if self.property_id.state in ('new', 'offer_received'):
            self.property_id.state = 'offer_accepted'
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse(self):
        self.ensure_one()
        if not self.status:
            self.status = 'refused'
        return True
