from odoo import api, exceptions, fields, models
from datetime import date, timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price",
                         required=True)

    status = fields.Selection(
                    [("accepted", "Accepted"),
                    ("refused", "Refused")],
                    string="Status",
                    copy=False )
                            
    partner_id = fields.Many2one("res.partner", 
                                string="Buyer",
                                required=True)

    property_id = fields.Many2one("estate.property",
                                 string="Property", 
                                 required=True)

    property_type_id = fields.Many2one(
                        "estate.property.type",
                        string="Property Type",
                        related="property_id.property_type_id", #have to search about this
                        store=True ) #have to search about this
                                    
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", 
                                inverse="_inverse_date_deadline", 
                                store=True ) 

    

    _sql_constraints = [('check_price', 'CHECK(price > 0)', 
                    'The offer price must be strictly positive.')]

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - create_date).days if record.date_deadline else 0
    
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise exceptions.UserError("This property is already sold.")
            
            # Ensure no other offer is accepted
            accepted_offers = self.env['estate.property.offer'].search([
                ('property_id', '=', record.property_id.id),
                ('status', '=', 'accepted')
            ])
            if accepted_offers:
                raise exceptions.UserError("Only one offer can be accepted per property.")
            
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'

    def action_refuse(self):
        for record in self:
            record.status = 'refused'

    


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            
            if property and property.best_offer:
                if vals['price'] < property.best_offer:
                    raise UserError(f"Offer should be higher than the current best offer of {property.best_offer}")
            
            property.state = 'offer_received'
        
        return super().create(vals_list)




