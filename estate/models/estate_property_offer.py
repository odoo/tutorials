# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Real Estate Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        ('check_price', "CHECK(price > 0)", "The price must be positive."),
    ]

    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string='Validity (days)', default=7)

    state = fields.Selection(selection=[
        ('accepted', "Accepted"),
        ('refused', "Refused"),
    ], string="Status", copy=False)

    partner_id = fields.Many2one(comodel_name='res.partner', string="Partner", required=True)
    property_id = fields.Many2one(comodel_name='estate.property', string="Property", required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True)

    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = date + relativedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - date).days

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env['estate.property'].browse(offer['property_id'])
            if property.state == 'sold':
                raise UserError(_("You can not create an offer for a sold property."))
            if property.offer_ids:
                max_offer = max(property.offer_ids.mapped('price'))
                partner_name = property.offer_ids.filtered(lambda x: x.price == max_offer).mapped('partner_id.name')[0]
                if float_compare(offer['price'], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError(_("The new offer must be higher than the maximum offer of %(max_offer).2f from %(partner_name)s.", max_offer=max_offer, partner_name=partner_name))
            if property.state != 'offer_received':
                property.state = 'offer_received'
        return super().create(vals_list)

    def action_accept(self):
        if 'offer_accepted' in self.mapped('property_id.state'):
            raise UserError(_("An offer has already been accepted."))
        elif 'sold' in self.mapped('property_id.state'):
            raise UserError(_("Cannot accept an offer for a sold property."))
        elif 'canceled' in self.mapped('property_id.state'):
            raise UserError(_("Cannot accept an offer for a canceled property."))
        for offer in self:
            offer.property_id.write({
                'state': 'offer_accepted',
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
            })
        return self.write({'state': 'accepted'})

    def action_refuse(self):
        return self.write({'state': 'refused'})
