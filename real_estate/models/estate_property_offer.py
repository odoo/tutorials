from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"

    price = fields.Float(required=True)
    status= fields.Selection(
        [('accepted', 'Accepted'),('refused','Refused')],
        string="Status",
        copy=False        
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property Name", required=True)
    validity= fields.Integer(string="Valid for", default=7)
    date_deadline= fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline", string="Offer Deadline ", default=date.today()+relativedelta(days=+7))
    property_type_id= fields.Many2one("estate.property.type", string="Property Type Id", related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0 )','The offer price should be positive and greater than 0.'),
        ('check_validity', 'CHECK(validity > 0 )','The validity cannot be negative.')
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            offer_price = vals.get('price')
            existing_offers = property_id.mapped("offer_ids")
            if property_id.status == 'sold' or property_id.status == 'offer_accepted':
                raise ValidationError(f"Offers cannot be created!!! Property already sold or offer already accepted!!!")
            if existing_offers:
                highest_offer = max(existing_offers, key=lambda o: o.price)
                if offer_price < highest_offer.price:
                    raise ValidationError(f"The offer price for {property_id.name} must be higher than the existing accepted offer of {highest_offer.price}.")
            property_id.status = "offer_received"
        return super().create(vals_list)

    @api.depends("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date==False:
                record.create_date=date.today()
            record.validity = (record.date_deadline-record.create_date.date()).days

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date==False:
                record.create_date=date.today()
            record.date_deadline = record.create_date.date() + relativedelta(days=+(record.validity))

    def accept_offer(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price=record.price
            record.property_id.buyer_id=record.partner_id
            for offer in self.property_id.offer_ids:
                if offer != self: 
                    offer.status = "refused"
            record.property_id.status="offer_accepted"
        return True
    
    def refuse_offer(self):
        for record in self:
            record.status = "refused"
        return True
