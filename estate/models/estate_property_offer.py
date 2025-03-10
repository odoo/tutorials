from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo.exceptions import UserError


class estate_Property_Offer(models.Model):
    _name = "estate.property.offer"
    _description = "relevent offers"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection([('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id = fields.Many2one("res.partner",required=True, string="Partner")
    property_id = fields.Many2one("estate.properties", required=True)
    validity =fields.Integer("Validity (days)",default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related = "property_id.property_ids", store = True)

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)','The price must be strictly positive.')
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = date.today() + relativedelta(days =+ record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - date.today()).days

    def action_accept(self):
        if self.property_id.selling_price:
            raise UserError("Another offer is already accepted")            
        else:
            self.status = "accepted"
            self.property_id.status = "offer accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price

            for record in self.property_id.offer_ids:
                if record != self: 
                    record.status = "refused" 
        
    def action_refuse(self):
        self.status = "refused"
        self.property_id.selling_price = 0
        self.property_id.buyer_id = False



