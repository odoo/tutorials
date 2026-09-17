from datetime import datetime, timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    price = fields.Float(string='Price')
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    property_type = fields.Many2one(related='property_id.property_type', string='Property type')
    status = fields.Selection(
        string='Status',
        readonly=True,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    validity = fields.Integer(string='Validity', default=7)

    _strictly_positive_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of an offer should be strictly positive',
    )

    def _compute_display_name(self):
        for record in self:
            record.display_name = self.env._("Estate Property Offer %s", self.id)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def accept_offer(self):
        for record in self:
            if any(offer.status == 'accepted' for offer in record.property_id.offers):
                raise UserError(self.env._('Only one offer can be accepted by property.'))
            record.status = 'accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
        return True

    def refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer = None
                record.property_id.selling_price = None
                record.property_id.state = 'offer_received'
            record.status = 'refused'
        return True

    def action_view_property(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property',
            'name': self.env._('Properties'),
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', '=', self.property_id.id)],
        }

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if float_compare(record.property_id.expected_price * 0.9, record.price, 2) == 1:
                raise ValidationError(self.env._(r'The price of an offer cannot be lower than 90% of the expected price of the property.'))

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id']).with_prefetch(self.ids)
            if any(offer.price > vals['price'] for offer in property.offers):
                raise UserError(self.env._('An offer cannot have a lower price than an existing offer.'))
            if property.state == 'new':
                property.state = 'offer_received'
        return super().create(vals_list)
