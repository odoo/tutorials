from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer for a property'
    _order = 'price desc'

    price = fields.Float(default=0.0)
    state = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='new', copy=False)

    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type', related='property_id.property_type_id', stored=True)

    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    create_date = fields.Date('Date Created')

    _sql_constraints = [
        ('check_price',
         'CHECK(price > 0)',
         'An offer\'s price must be positive')
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = \
                record.create_date + relativedelta(days=record.validity) \
                    if record.create_date and record.validity != None else None

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days

    def action_accept(self):
        for record in self:
            if record.state == 'accepted':
                continue

            if record.property_id.selling_price:
                raise UserError('The property already has an accepted offer!')

            record.property_id._accept_offer(record)
            record.state = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            if record.state == 'accepted':
                record.property_id._refuse_accepted_offer()

            record.state = 'refused'
        return True
    
    @api.model
    def create(self, vals):
        self.env['estate.property'].browse(vals['property_id']).exists().state = 'offer_received'
        return super().create(vals)
