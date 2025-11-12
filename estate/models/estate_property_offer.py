# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.tools.float_utils import float_compare
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Estate Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        ('check_offer_price', "CHECK(price > 0)", "offer price must be strictly positive.")
    ]

    price = fields.Float(string="Price")
    status = fields.Selection([
        ('accepted', "Accepted"),
        ('refused', "Refused")
    ], string="Status", copy=False)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True, string="Partner")
    property_id = fields.Many2one(comodel_name='estate.property', required=True, string="Property")
    property_type_id = fields.Many2one('estate.property.type', string="Property Type", related='property_id.property_type_id', store=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute='_compute_date_deadline', inverse='_inverse_date_deadline', store=True)

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env['estate.property'].browse(offer['property_id'])
            if property.state == 'sold_offer':
                raise UserError(_(f"You cannot create an offer for a sold property"))
            existing_offers = property.offer_ids.mapped('price')
            max_offer = max(existing_offers) if existing_offers else 0
            partner_name = property.offer_ids.filtered(lambda x: x.price == max_offer).mapped('partner_id.name')
            partner_name = partner_name[0] if partner_name else "Unknown"
            if float_compare(offer['price'], max_offer, precision_rounding=0.01) <= 0:
                raise UserError(_("The new offer must be higher than the maximum offer of %(max_offer).2f from %(partner_name)s.", max_offer=max_offer, partner_name=partner_name))
        return super().create(vals_list)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date.date() if offer.create_date else fields.Date.today()
            offer.validity = (offer.date_deadline - create_date).days

    def action_accept(self):
        if any(self.filtered(lambda offer: offer.property_id.state == 'offer_accepted' or offer.status == 'accepted')):
            raise UserError(_("Offer has already been accepted!"))
        self.write({'status': 'accepted'})
        self.mapped('property_id').write({
            'state': 'offer_accepted',
            'selling_price': self.price,
            'buyer_id': self.partner_id,
        })
        return True

    def action_refuse(self):
        if self.status == 'refused':
            raise UserError(_("Offer has already been refused!"))
        self.write({'status':'refused'})
        return True
