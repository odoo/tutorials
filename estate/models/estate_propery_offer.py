from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer received for a property from partner'
    _order = 'price desc'

    price = fields.Float('Price')
    status = fields.Selection(string='Status', selection=[(
        'accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(
        string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Offer Price must be strictly positive'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = (record.create_date if hasattr(
                record, 'create_date') and record.create_date else datetime.now()) + timedelta(days=record.validity)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            property.state = 'offer_received'
            if vals['price'] < property.best_offer:
                raise UserError(
                    f"The price must be higher than {property.best_offer}")
        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            deadline = (record.date_deadline - record.create_date.date()).days
            record.validity = 0 if deadline < 0 else deadline

    def action_accept(self):
        property = self.property_id
        property.write({
            'buyer': self.partner_id,
            'selling_price': self.price,
            'state': 'offer_accepted',
        })
        self.status = 'accepted'

        # Refusing other offers so only one can be accepted.
        other_offers = property.offer_ids - self
        other_offers.write({
            'status': 'refused',
        })

    def action_reject(self):
        self.status = 'refused'
