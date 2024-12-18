
from odoo import fields, models
from odoo.api import depends, onchange
from odoo.tools.date_utils import date, relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "An offer for a real estate property"

    price = fields.Float()
    status = fields.Selection(
            string="Status",
            selection=[('refused', 'Refused'), ('accepted', 'Accepted')]
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_compute_validity")
    partner_id = fields.Many2one("res.partner", string="Partner", required=True, copy=False)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    @depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity) if record.create_date else date.today()

    def _compute_validity(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
