from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class EstatePropertyOffer(models.Model): 
    _name = "estate.property.offer"
    _description = "Offer for a property"
    
    price = fields.Float(string="Price", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True, help="The property this offer is for")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, help="The partner making the offer")
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
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id
            }
        )
        
    def action_refuse(self):
        return self.write({"status":"refused"})    
                        
                       
    