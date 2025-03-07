# Part of Odoo. See LICENSE file for full copyright and licensing details. 

from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Property Offer"
    _order = 'price desc'
    _sql_constraints = [
        ('check_offer_price', "CHECK(price > 0)", "The offer price must be strictly positive."),
    ]

    price = fields.Float(string= "Price")
    status = fields.Selection(
        selection=[  
            ('accepted', "Accepted"),  
            ('refused', "Refused")  
        ],  
        string="Status",  
        copy=False  
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner', 
        string="Partner", 
        required=True
    )
    property_id = fields.Many2one(
        comodel_name='estate.property', 
        string="Property", 
        required=True , 
        ondelete='cascade'
    )
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(
        compute = '_compute_date_deadline', 
        inverse = '_inverse_date_deadline'
    )
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type', 
        related='property_id.property_type_id', 
        string="Property Type", 
        store=True
    )
    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date  or fields.Date.today()) + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity=(offer.date_deadline - fields.Date.today()).days or 0

    def action_accept(self):
        if self.status == 'accepted':
            raise UserError(_("Offer has already been accepted!"))
            return
        self.write({'status':'accepted'})
        for property in self.mapped('property_id'):
            property.write({
                'state': 'offer_accepted',
                'selling_price': self.price,
                'buyer_id': self.partner_id,
            })

    def action_refuse(self):    
        if self.status == 'refused':
            raise UserError(_("Offer has already been refused!"))
        self.write({'status':'refused'})

    @api.model_create_multi
    def create(self, vals_list):
        for offer in vals_list:
            property = self.env['estate.property'].browse(offer['property_id'])
            if property.state == 'sold':
                raise UserError(_("You cannot create an offer for a sold property"))
            if property.state != 'offer_received':
                property.state = 'offer_received'
            existing_offers = property.property_offer_ids.mapped('price')
            max_offer = max(existing_offers) if existing_offers else 0
            if property.property_offer_ids and offer['price'] <= max_offer:
                raise UserError(_(f"The new offer must be higher than the maximum offer of {max_offer:.2f}"))
        return super().create(vals_list)
