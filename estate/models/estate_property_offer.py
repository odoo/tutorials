from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(copy=False, string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True)

    _sql_constraints = [
        ('check_strict_positive_price',
            'CHECK(price > 0)',
            'The price should be strictly positive'),
    ]

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = fields.Date.to_date(record.create_date or fields.Date.today())
            record.validity = (record.date_deadline - create_date).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError(message='The property has already an accepted offer')
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.property_id.buyer_id == record.partner_id:
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0
                record.property_id.state = 'new'
            record.status = 'refused'
        return True
