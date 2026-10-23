from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        string='Status',
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Date Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id',
                                       string='Property Type', store=True)

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The price of property offer must be strictly positive',
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        self.ensure_one()
        self.status = 'accepted'
        property_id = self.property_id
        property_id.selling_price = self.price
        property_id.buyer_id = self.partner_id

    def action_refuse(self):
        self.ensure_one()
        self.status = 'refused'

    @api.model
    def create(self, vals_list):
        property_ids = set()

        for val in vals_list:
            if val.get('property_id'):
                property_ids.add(val['property_id'])

        properties = self.env['estate.property'].browse(property_ids)

        property_by_id = {
            prop.id: prop for prop in properties
        }

        for val in vals_list:
            singleton_property = property_by_id.get(val.get('property_id'))

            if singleton_property and val['price'] < singleton_property.best_price:
                raise ValidationError('The price of property offer must be greater than the best price')

        offers = super().create(vals_list)

        offers.mapped('property_id').filtered(lambda prop: prop.state != 'offer_received').write(
            {'state': 'offer_received'})

        return offers
