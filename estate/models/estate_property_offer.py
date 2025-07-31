from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate offers"
    _order = "price desc"

    price = fields.Float(required=True, string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], copy=False, string='Status')
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7, string='Validity')
    date_deadline = fields.Date(compute='_compute_date_dealine', inverse='_inverse_date_deadline', string='Deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)',
         'The offer price for a property must be strictly positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_dealine(self):
        for record in self:
            create_date = record.create_date and record.create_date or fields.Date.today()
            record.date_deadline = create_date + relativedelta(days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            if record.property_id.state in ['new', 'offer received']:
                record.property_id.state = 'offer accepted'
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
                record.status = 'accepted'
            else:
                raise UserError("An offer has already been accepted or the property was cancelled.")

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = self.env['estate.property'].browse([vals['property_id'] for vals in vals_list])
        for vals in vals_list:
            property_id = property_ids.filtered(lambda p: p.id == vals['property_id'])
            max_existing_offer = property_id.best_price
            if vals['price'] < max_existing_offer:
                raise UserError(f"An offer price {vals['price']} should not be less than an existing offer {max_existing_offer}.")
            else:
                property_id.state = 'offer received'
        return super().create(vals_list)
