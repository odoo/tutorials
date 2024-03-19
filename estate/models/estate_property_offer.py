"""module for the estate property offer model"""

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

class EstatePropertyOffer(models.Model):
    "Estate property type odoo model"
    _name = "estate.property.offer"
    _description= "model for real estate asset types (e.g. house)"
    #
    price = fields.Float("Price")
    status = fields.Selection(
            [("accepted", "Accepted"), ("refused", "Refused")],
            string = "Status",
            copy = False)
    partner_id = fields.Many2one('res.partner', required = True, string = "Prospective Buyer")
    property_id = fields.Many2one('estate.property', required = True, string = "Property")
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_date_deadline", inverse="_inverse_date_deadline")
    #
    @api.depends("validity", "create_date")
    def _date_deadline(self):
        start_date = self.create_date or fields.Date.today()
        self.date_deadline = start_date + relativedelta(days = self.validity)
    #
    def _inverse_date_deadline(self):
        end, start = fields.Date.to_date(self.date_deadline), fields.Date.to_date(self.create_date)
        self.validity = (end - start).days
    #

