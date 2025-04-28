from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offers'
    _order = 'price desc'

    price = fields.Float('Price', default=0.0)
    status = fields.Selection(
        string='Status',
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused'),
        ],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date(
        'Deadline',
        compute='_compute_deadline',
        inverse='_inverse_deadline',
    )
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _sql_constraints = [
        (
            'check_price',
            'CHECK(price >= 0)',
            'An offer price must be strictly positive.',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if (
                float_compare(
                    max(property_id.offer_ids.mapped('price'), default=-0.01), vals['price'], precision_digits=3
                )
                > -1
            ):
                raise UserError(_("Can't create an offer with a lower amount than an other offer"))
        property_id.write(
            {
                'state': 'received',
            }
        )
        return super().create(vals_list)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_state_accept(self):
        for record in self:
            if record.property_id.offer_ids.filtered(lambda offer: offer.status == 'accepted'):
                raise UserError(_('Only one offer can be accepted for a given property'))
            record.status = 'accepted'
            record.property_id.write(
                {
                    'selling_price': record.price,
                    'buyer_id': record.partner_id,
                }
            )
        return True

    def action_state_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
