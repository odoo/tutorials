from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from .helper import format_selection


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _order = 'price desc'
    _description = 'Offer modelisation'
    _sql_constraints = [('offer_price_strictly_positive', 'CHECK(price > 0)', 'Offer price must be stricly positive')]

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(copy=False, selection=format_selection(['accepted', 'refused']), string='Status')
    partner_id = fields.Many2one('res.partner', required=True, string='Buyer')
    property_id = fields.Many2one('estate.property', required=True, string='Property')

    validity = fields.Integer(default=7, string="Validity")  # in days
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Deadline')

    property_type_id = fields.Many2one(related='property_id.property_type_id', string='Property type')

    @api.depends('validity')
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - fields.Date.today()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if any(vals['price'] < offer.price for offer in property_id.offer_ids):
                raise UserError(_('Offer price must be higher than existing offers.'))
            property_id.state = 'offer received'
        return super().create(vals_list)

    def action_accept(self):
        self.ensure_one()
        if self.property_id.state == 'sold':
            raise UserError(_('The house was already sold.'))
        self.status = 'accepted'
        self.property_id.state = 'offer accepted'
        self.property_id.buyer_id = self.partner_id
        self.property_id.se.selling_price):
            raise UserError(_('Customer or selling price was not set.'))
'refused'
        return True
