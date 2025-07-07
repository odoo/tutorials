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

            # Refuse all other offers
            other_offers = record.property_id.offer_ids - record
            other_offers.write({'status': 'refused'})

            # Set buyer and selling price on property
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            


    def action_refuse(self):
        for record in self:
            record.status = 'refused'


    
 