from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "this is the estate property offer model"
    _sql_constraints = [
        (
            'check_positive_amounts',
            'CHECK (price > 0)',
            'This amount must be positive',
        ),
    ]
    _order = 'price desc'

    price = fields.Float(digits=(20,2))
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    status = fields.Selection(
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False, readonly=True
    )
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related='property_id.property_type_id', store=True, string='Property Type')
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)
            else:
                record.date_deadline = record.create_date.date() + relativedelta(days=record.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if not record.create_date:
                record.validity = (record.date_deadline - fields.Date.today()).days
            else:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True

    # TODO: should maybe modify vals_list variable and then call super().create
    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        for record in records:
            if float_compare(record.price, record.property_id.best_price, precision_digits=10) < 0:
                raise UserError("Creating an offer which is worse than another is not allowed")
            record.property_id.state = 'received'
        return records
