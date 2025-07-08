from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers related to property are made"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refuse')],
        copy = False,
    )
    partner_id = fields.Many2one(
        "res.partner",string='Partner',index = True,  default = lambda self: self.env.user.partner_id.id
)
    property_id = fields.Many2one("estate.property",index = True, required = True)
    validity = fields.Integer(default = 7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The offer price must be greater than 0')
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            # Use create_date if available, otherwise fallback to today
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            if record.date_deadline:
                record.validity = (record.date_deadline.day - create_date.day)
                
    def action_confirm(self):
        for record in self:
            # Ensure only one accepted offer per property
            if any(
                offer.status == 'accepted'
                for offer in record.property_id.offer_ids
            ):
                raise UserError("Only one offer can be accepted per property.")

            
            min_price = record.property_id.expected_price * 0.9
            if float_compare(record.price, min_price, precision_digits=2) < 0:
                raise ValidationError("Offer must be at least 90% of the expected price to be accepted.")
        
            record.status = 'accepted'
            record.property_id.state = 'offer accepted'

            # Refuse all other offers
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})

            # Set buyer and selling price on property
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
            

    @api.model
    def create(self, vals):
        # Get the property object using the ID in vals
        offer = super().create(vals)
        property_id = vals.get('property_id')
        new_price = vals.get('price', 0)
        property_rec = self.env['estate.property'].browse(property_id)

        # Check if the offer is lower than any existing offers
        existing_prices = property_rec.offer_ids.mapped('price')
        if existing_prices and new_price < max(existing_prices):
            raise ValidationError("Offer price must be higher than existing offers.")

        # Set state to 'offer received' if it’s currently 'new'
        if property_rec.state == 'new':
            property_rec.state = 'offer received'
        return offer
    _order = "price desc"

    property_type_id = fields.Many2one('estate.property.type',index = True)
    
 