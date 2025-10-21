from odoo import api, models, fields
import datetime


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for properties"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True, string="Partner")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    create_date = fields.Date(copy=False, default=lambda self : datetime.date.today(), readonly=True)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")


    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(offer.create_date, days=offer.validity)


    def _inverse_deadline(self):
        for offer in self:
            delta = offer.date_deadline - offer.create_date
            offer.validity = delta.days
