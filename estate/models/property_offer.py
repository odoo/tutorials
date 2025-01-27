from odoo import api,fields, models
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "reals estate properties offer"

    property_type_id= fields.Char('Property Offer ID')
    price = fields.Float('Le Prix')
    status = fields.Selection([("Accepted","Accepted"),("Refused","Refused")],copy=False)
    partner_id=fields.Many2one("res.partner",required=True)
    property_id=fields.Many2one("estate.property",required=True)
    validity= fields.Integer(default=7)
    date_deadline=fields.Date(compute="_compute_deadline",inverse="_inverse_deadline",string="Date Limite")


    @api.depends("validity")
    def _compute_deadline(self):
        for record in self: 
            if record.create_date:
                record.date_deadline=record.create_date+timedelta(days=record.validity)
            else : record.date_deadline=date.today()+timedelta(days=record.validity)
        
    def _inverse_deadline(self):
        for record in self: 
            date_crea = fields.Date.to_date(record.create_date or fields.Date.today())
            record.validity=(record.date_deadline-date_crea).days
