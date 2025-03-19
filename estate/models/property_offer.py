from odoo import api,fields, models,exceptions
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "reals estate properties offer"

    property_offer_id= fields.Char('Property Offer ID')
    price = fields.Float('Le Prix')
    status = fields.Selection([("Accepted","Accepted"),("Refused","Refused")],copy=False)
    partner_id=fields.Many2one("res.partner",required=True)
    property_id=fields.Many2one("estate.property",required=True)
    validity= fields.Integer(default=7)
    date_deadline=fields.Date(compute="_compute_deadline",inverse="_inverse_deadline",string="Date Limite")
    offer_type_id=fields.Many2one(related="property_id.property_type_id")
    
    _order="price desc"


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
    
    def offer_accepted(self):
        if "Accepted" in self.property_id.offer_ids.mapped('status'):
            raise exceptions.UserError("An other offer has already been accepted")
        else : 
            for record in self: 
                record.status="Accepted"
                record.property_id.buyer_id=record.partner_id
                record.property_id.selling_price=record.price
            return True

    def offer_declined(self):
        for record in self:
            record.status="Refused"
        return True

    _sql_constraints = [
        ('offer_price_positive', 'CHECK(price >= 0)',
         'The offer price hase to be positive'),
    ]

    @api.model_create_multi
    def create(self, vals):
        for val in vals: 
            if val['price'] < self.env['estate.property'].browse(val['property_id']).best_price:
                raise exceptions.UserError("Can't make an offer this low")
            self.env['estate.property'].browse(val['property_id']).state="Offer Received"
        return super().create(vals)
