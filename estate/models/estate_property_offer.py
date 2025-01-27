from odoo import models, fields, api, exceptions
from datetime import date, timedelta

class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "The offers for a property"

    price = fields.Float(name = "Price", required = True)
    status = fields.Selection(string='Status',
        selection=[('accepted', 'Accepted'), 
                   ('refused', 'Refused'), 
                   ],
        help="What was the answer to the offer ?")
    partner_id = fields.Many2one("res.partner", required=True, name="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(name="Validity", default=7)
    date_deadline = fields.Date(name="Deadline", compute="_compute_deadline", inverse="_inverse_validity")
    _sql_constraints = [
    ('positive_offer_price', 
     'CHECK(price > 0)', 
     'The offer price must be strictly positive!')
]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if isinstance(record.create_date, fields.Date):
                record.date_deadline = record.date_deadline + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_validity(self):
        for record in self:
            if isinstance(record.create_date, fields.Date):
                record.validity = (record.date_deadline - record.create_date).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_reject_offer(self):
        self.status = "refused"
    def action_accept_offer(self):
        if not self.property_id.get_status():
            self.status = "accepted"
            self.property_id.set_buyer(self.partner_id)
            self.property_id.set_status("sold")
            self.property_id.set_sold_price(self.price)
        else:
            raise exceptions.UserError("This property has already been sold !")
