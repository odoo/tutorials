from odoo import api, models, fields # type: ignore
from odoo.exceptions import ValidationError # type: ignore
from datetime import date
from dateutil.relativedelta import relativedelta

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
    date_deadline= fields.Date(compute="_compute_date_deadline", inverse="_compute_validity",string="Offer Deadline ", default=date.today()+relativedelta(days=+7))

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0 )',
         'The offer price should be positive and greater than 0.')
    ]

    @api.depends("date_deadline")
    def _compute_validity(self):
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
            record.property_id.buyer_user_id=record.partner_id
        return True
    
    def refuse_offer(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price=False
            record.property_id.buyer_user_id=False
        return True
