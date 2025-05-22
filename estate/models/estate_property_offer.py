from dateutil.relativedelta import relativedelta
from odoo import api, exceptions, fields, models


class EstateOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'It allows to create a new property offer'
    _order = 'price desc'

    price = fields.Float(required=True)
    validity = fields.Integer()
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date')
    create_date = fields.Date(default=fields.Date.today(), required=True)
    partner_id = fields.Many2one('res.partner', string='Customer')
    property_id = fields.Many2one('estate.property', string='Property')
    status = fields.Selection(
        string='State',
        selection=[
            ('pending', 'Pending'),
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        default='pending',
    )

    _sql_constraints = [('price', 'CHECK(price >= 0 )', 'A price should always be possitive')]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_date(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state not in ['sold', 'cancelled']:
                for offer in record.property_id.offer_ids:
                    offer.status = 'refused'
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.state = 'offer accepted'
            else:
                raise exceptions.UserError('property already cancelled')
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.property_id.state not in ['sold', 'cancelled']:
                if record.status == 'accepted':
                    record.property_id.selling_price = 0
                    record.property_id.state = 'offer received'
            else:
                raise exceptions.UserError('property already sold or cancelled')
            record.status = 'refused'
        return True
