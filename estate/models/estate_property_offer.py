from odoo import models, fields, api
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
