from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offers'
    _order = 'price desc'

    price = fields.Float('Price', required=True)
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
            'CHECK(price > 0)',
            'An offer price must be strictly positive.',
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.best_price and (float_compare(property_id.best_price, vals['price'], precision_digits=3) > 0):
                raise UserError(_("Can't create an offer with a lower amount than an other offer"))
        property_id.write({'state': 'received',})
        return super().create(vals_list)

    @api.depends('validity')
    def _compute_deadline(self):
        for r_offer in self:
            base_date = r_offer.create_date or fields.Date.today()
            r_offer.date_deadline = base_date + relativedelta(days=r_offer.validity)

    def _inverse_deadline(self):
        for r_offer in self:
            base_date = r_offer.create_date or fields.Date.today()
            r_offer.validity = (r_offer.date_deadline - base_date.date()).days

    def action_state_accept(self):
        for r_offer in self:
            if r_offer.property_id.state == 'accepted':
                raise UserError(_('Only one offer can be accepted for a given property'))
            r_offer.property_id.offer_ids.status = 'refused'
            r_offer.status = 'accepted'
            r_offer.property_id.write(
                {
                    'selling_price': r_offer.price,
                    'buyer_id': r_offer.partner_id,
                    'accepted': r_offer.property_id.state
                }
            )
        return True

    def action_state_refuse(self):
        for r_offer in self:
            r_offer.status = 'refused'
        return True
