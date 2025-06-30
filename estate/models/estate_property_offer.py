from odoo import models, fields, api
from datetime import date, timedelta
from odoo.tools import float_compare
from odoo.exceptions import UserError, ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        string="Status",
        required=True,
        default="refused",
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Partner",
        required=True,
    )
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
        required=True,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline", 
        store = True,       
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = date.today() + timedelta(days=offer.validity) 

    def _inverse_date_deadline(self):
        for offer in self:            
            offer.validity = (offer.date_deadline - date.today()).days

    def action_accept(self):
        if 'accepted' in self.mapped('property_id.offer_ids.status'):
            raise ValueError("There is already an accepted offer for this property.")
        self.write({'status': 'accepted'})
        return self.mapped('property_id').write({
            'state': 'offer_accepted',
            'selling_price': self.price,
            'buyer_id': self.partner_id.id,
        })
        

    def action_refuse(self):
        self.status = 'refused'

    @api.model
    def create(self, vals):
        new_offer = vals.get('price', 0.0)
        property_id = vals.get('property_id')
        if property_id:
            property = self.env['estate.property'].browse(property_id)
            if float_compare(new_offer, property.best_price, precision_rounding=0.01) <= 0:
                raise ValidationError("Offer price must be higher than the best price of the property.")
        return super(EstatePropertyOffer, self).create(vals)