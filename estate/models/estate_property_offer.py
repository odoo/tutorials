from odoo import api, fields, models
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
    property_id = fields.Many2one("estate.property", required=True)
    validity =fields.Integer("Validity (days)",default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(related = "property_id.property_ids", store = True)

    _sql_constraints = [
        ('price', 'CHECK(price > 0)','The price must be strictly positive.')
    ]

    @api.constrains('date_deadline')
    def _check_date_deadline(self):
        for record in self:
            if record.date_deadline < fields.Date.today():
                raise models.ValidationError("The deadline date cannot be in the past. Please choose a future date.")

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
            self.property_id.status = "offer_accepted"
            self.property_id.buyer_id = self.partner_id
            self.property_id.selling_price = self.price

            for record in self.property_id.offer_ids:
                if record != self: 
                    record.status = "refused" 
        
    def action_refuse(self):
        self.status = "refused"
        self.property_id.selling_price = 0
        self.property_id.buyer_id = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            if property_id.status == 'sold':
                raise UserError("You cannot create an offer for a sold property.")
            offer_price = vals.get('price')
            existing_offers = property_id.mapped("offer_ids")
            if existing_offers:
                highest_offer = max(existing_offers, key=lambda o: o.price)
                if offer_price <= highest_offer.price:
                    raise UserError(f"The offer price must be higher than the existing accepted offer of {highest_offer.price}.")
            property_id.status = "offer_received"
        return super().create(vals_list)
