from odoo import api, models, fields
from datetime import timedelta

class EstatePropertyOffer (models.Model): 
    _name = "estate.property.offer"
    _description = "Lời đề nghị"
    
    price  = fields.Integer( string="Price")
    validity  = fields.Integer( string="Validity (days)", default=7 )
    date_deadline  = fields.Date( string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)
    status = fields.Selection(selection=[("new", "New"),
            ("offerReceived", "Offer Received")], string="Status" )
    partner_id  = fields.Many2one("res.partner", string="Partner")
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
         if record.create_date:
          base_date = record.create_date.date()
         else :
          base_date = fields.Date.today()
         record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
         if record.create_date:
          base_date = record.create_date.date()
         else :
          base_date = fields.Date.today()
         diff = record.date_deadline - base_date
         record.validity = max(0, diff.days)

    def action_confirm(self):
        for record in self:
         return True
