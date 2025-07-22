from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
from odoo.tools import float_compare

class EstatePropertyOffer(models.Model): 
    _name = "estate.property.offer"
    _description = "Offer for a property"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "The expected price must be strictly positive")
    ]
    
    price = fields.Float(string="Price", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, help="The property this offer is for")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, help="The partner making the offer")
    property_type_id = fields.Many2one("estate.property.type", string="Property Type", related="property_id.property_type_id", store=True)
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], string="Status", copy=False)
    validity = fields.Integer(string="Validity(days)", default=7, help="Number of days this offer is valid")
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", help="Date when offer expires")
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                # if the record existis and it has a create_date
                record.date_deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                # using today's date if record isn't created yet
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)
    
    
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                if record.create_date:
                    difference = record.date_deadline - record.create_date.date()
                    record.validity = difference.days
                else:
                    #  using today's date again
                    difference = record.date_deadline - fields.Date.today()
                    record.validity = difference.days
    
    def action_accept(self):
        # check if record with status accepted already exists
        # if it exists raise error saying an offer was already accepted
        # self.write status accepted
        # self.write property with status, selling price and buyer id
        if "accepted" in self.mapped("property_id.offer_ids.status"):
            raise UserError("An offer was already accepted")
        self.write(({"status":"accepted"}))
        return self.mapped("property_id").write(
            {
                "state":"offer accepted",
                "selling_price":self.price,
                "buyer_id":self.partner_id
            }
        )
        
    def action_refuse(self):
        return self.write({"status":"refused"})    
    
    @api.model
    def create(self, vals): 
        property_id = vals.get("property_id")
        if not property_id:
            raise ValidationError("Property is required for offer creation")
        
        # Browsing in order to get the property record
        property_record = self.env['estate.property'].browse(property_id)
        
        # checking if there are any existing offer for the record 
        existing_offers = self.search([("property_id", "=", property_id)])
        
        # getting max offer and comparing with the current price 
        if existing_offers: 
            max_existing_offer = max(existing_offers.mapped("price"))
            new_price = vals.get("price", 0)
            
            if float_compare(new_price, max_existing_offer, precision_digits=2) <= 0:
                raise UserError(
                    f"Offer amount ({new_price:,.2f}) must be higher than "
                    f"existing offers (highest: {max_existing_offer:,.2f})"
                )
        
        # creating the offer 
        offer = super().create(vals)
        
        # updating the state when an offer is added 
        
        if property_record.state == "new":
            property_record.write({"state": "offer received"})
        
        return offer    
                
            
        
        
        
                        
                       
    