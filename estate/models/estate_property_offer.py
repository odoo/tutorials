from datetime import timedelta
from odoo import api, fields, models


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
