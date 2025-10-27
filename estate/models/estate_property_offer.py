from dateutil.relativedelta import relativedelta

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float(string='price', required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'),
        ('refused', 'Refused')],
        string="Status",
        copy=False,
        # default='accepted',
    )
    validity = fields.Integer(string='Validity(days)', default=7)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', store=True)
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True, string="Property Type")

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for offer in self:
            if not offer.create_date:
                offer.date_deadline = fields.Date.today() + relativedelta(days=offer.validity)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id") and vals.get("price"):
                prop = self.env["estate.property"].browse(vals["property_id"])
                
                if float_compare(vals["price"], prop.expected_price * 0.9, precision_rounding=0.01) < 0:
                    raise UserError("The offer price must be at least 90%% of the expected price.")

                if prop.offer_ids:
                    max_offer = max(prop.mapped("offer_ids.price"))
                    if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                        raise UserError("The offer must be higher than %.2f" % max_offer)

        new_offers = super().create(vals_list)

        for offer in new_offers:
            offer.property_id.state = "offer_received"
        
        return new_offers

    def action_accept(self):
        print("Accepting offer...")
        for offer in self:
            if any(prop_offer.status == 'accepted' for prop_offer in offer.property_id.offer_ids):
                raise UserError("An offer has already been accepted for this property.")
            if offer.status == 'refused':
                raise UserError("A refused offer cannot be accepted.")
        else:
            offer.status = 'accepted'
            offer.property_id.write({
                'state': 'offer_accepted',
                'selling_price': offer.price,
                'buyer_id': offer.partner_id.id,
            })
        return True

    def action_refuse(self):
            if any(offer.status == 'accepted' for offer in self):           
                raise UserError("An accepted offer cannot be refused.")
            self.status = 'refused'
            return True
