# type: ignore
from datetime import timedelta
from odoo import api, exceptions, fields, models 
from odoo.exceptions import UserError 


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price=fields.Float(string="Price")
    status=fields.Selection(
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused')
    ])
    partner_id=fields.Many2one(
        'res.partner',
        string="Partner",
        required=True, 
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True,
        string="Property",
        ondelete="cascade"
    )
    validity = fields.Integer(
        string="Validity(Days)",
        default="7"
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
    )

    #sql constraints
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.'),
    ]

    #compute dealine
    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = 7

    #logic for offer accepted or refused
    def action_accept_offer(self):
        if self.property_id.status == 'offer_accepted':
                raise UserError("This property already has an accepted offer!")

        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        self.property_id.status = "offer_accepted"
        other_offers = self.property_id.offer_ids.filtered(lambda o: o.id != self.id)
        other_offers.write({'status': 'refused'})
    
    #Refuse an offer.
    def action_refuse_offer(self):
         self.status = "refused"
        
    
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals.get('property_id'))
            if property:
                property.status = 'offer_received'

            # Logic for the creation greater offer than previous
            existing_offers = property.mapped('offer_ids.price')
            if existing_offers and vals['price'] < max(existing_offers):
                raise exceptions.UserError("You cannot create an offer with a lower price than an existing offer.")
        return super().create(vals_list)
