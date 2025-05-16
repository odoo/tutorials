from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare, float_is_zero

from ..constants import PROPERTY_PRICE_PRECISION_EPSILON


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'the offer of the property being sold'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(selection = [('accepted', 'Accepted'), ('refused', 'Refused')], copy = False)
    partner_id = fields.Many2one('res.partner', string = 'Partner', required = True)
    property_id = fields.Many2one('estate.property', string = 'Property', required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(compute = '_compute_date_deadline', inverse = '_inverse_date_deadline')
    property_type_id = fields.Many2one(related = 'property_id.property_type_id', store = True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days = record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = fields.Date.from_string(record.create_date)
                record.validity = (record.date_deadline - create_date).days

    def action_accept_offer(self):
        self.ensure_one()
        if self.property_id.buyer_id:
            raise UserError('This property already has an accepted offer')
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'
        self.status = 'accepted'
        self.property_id.buyer_id = self.partner_id
        return True

    def action_refuse_offer(self):
        self.ensure_one()
        if self.property_id.buyer_id == self.partner_id:
            self.property_id.buyer_id = False
            self.property_id.state = 'offer_received'
            self.property_id.selling_price = 0
        self.status = 'refused'
        return True

    @api.model_create_multi
    def create(self, vals_list):
        property_offers = [vals for vals in vals_list if vals.get('property_id')]
        for offer_vals in property_offers:
            property_id = self.env['estate.property'].browse(offer_vals.get('property_id'))
            max_price = max(property_id.offer_ids.mapped('price'), default = 0.0)
            if float_compare(
                offer_vals.get('price'), max_price, precision_rounding = PROPERTY_PRICE_PRECISION_EPSILON
                ) < 0:
                raise UserError('The offer must be at least %s' % max_price)
            property_id.state = 'offer_received'
        return super().create(vals_list)

    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'Price must be positive')
    ]
