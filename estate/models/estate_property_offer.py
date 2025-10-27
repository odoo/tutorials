from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


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

    def action_accept(self):
        print("Accepting offer...")
        for offer in self:
            if any(prop_offer.status == 'accepted' for prop_offer in offer.property_id.offer_ids):
                raise UserError("An offer has already been accepted for this property.")
            if offer.status == 'refused':
                raise UserError("A refused offer cannot be accepted.")
            else:
                offer.status = 'accepted'
                offer.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
            if any(offer.status == 'accepted' for offer in self):           
                raise UserError("An accepted offer cannot be refused.")
            self.status = 'refused'
            return True
