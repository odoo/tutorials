from odoo import fields, models, api
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
                       
    