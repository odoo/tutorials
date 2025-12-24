from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "A property offer"
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(selection=[
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
        ], copy=False, string='Status')
    property_buyer_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_validity')

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.'
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            starting_date = record.create_date if record.create_date else fields.Date.context_today(self)
            record.date_deadline = starting_date + relativedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            starting_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.context_today(self)
            record.validity = (record.date_deadline - starting_date).days

    def action_accept(self):
        for record in self:
            match record.property_id.state:
                case 'offer_accepted':
                    raise UserError(_('This property already has an offer accepted'))
                case 'sold':
                    raise UserError(_('Sold properties cannot accept offers'))
                case 'cancelled':
                    raise UserError(_('Cancelled properties cannot accept other offers'))
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.property_buyer_id = record.property_buyer_id
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            record.property_id.property_buyer_id = None
            record.property_id.selling_price = 0

    @api.model
    def create(self, vals_list):
        for val in vals_list:
            self.env['estate.property'].browse(val['property_id']).check_create_offer(val['price'])
        return super().create(vals_list)
