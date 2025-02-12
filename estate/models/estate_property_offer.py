from odoo import models,fields, api, exceptions
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Real Estate Property Offer Model"
    _order = "price desc"

    price=fields.Float(required=True)
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner',required=True, string="Partner")
    create_date = fields.Date(default=fields.Date.today)
    property_id=fields.Many2one('estate.property',required=True)
    property_type_id=fields.Many2one(related='property_id.property_type_id',store=True)
    validity = fields.Integer(default = 7, string = "Validity (days)")
    date_deadline = fields.Date(string="Deadline", compute = "_compute_date_deadline", inverse="_inverse_date_deadline", store = True)

    @api.depends("create_date","validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            if record.property_id.status == "sold":
                raise exceptions.UserError("This property is already sold")
            if record.property_id.status == "cancelled":
                raise exceptions.UserError("This property is already cancelled")
            accepted_offer = self.search([
                    ('property_id', '=', record.property_id.id),
                    ('status', '=', 'accepted')
                ]   )
            if accepted_offer:
                raise exceptions.UserError("Only one offer can be accepted per property!")
            if record.price < (record.property_id.expected_price*0.9):
                raise exceptions.UserError("The selling price cannot be lower than 90% of the expected price.")
            record.status = "accepted"
            record.property_id.status = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

    def action_refuse(self):
        for record in self:
            if record.property_id.status == "sold":
                raise exceptions.UserError("This property is already sold")
            if record.property_id.status == "cancelled":
                raise exceptions.UserError("This property is already cancelled")
            record.status = "refused"
            if record.property_id.status == "offer_accepted":
                pass
            else:
                record.property_id.status = "offer_received"

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be strictly positive.')
    ]
