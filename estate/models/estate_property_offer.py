from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "It is a estate property offer model"

    price = fields.Float()
    status = fields.Selection([("Accepted", "Accepted"), ("Refuse", "Refuse")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_date_validity")
    create_date = fields.Date(default=date.today())

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_date_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date).days
