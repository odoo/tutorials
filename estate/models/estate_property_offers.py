from datetime import date
from dateutil.relativedelta import relativedelta
from odoo import api
from odoo import fields
from odoo import models


class PropertyOffer(models.Model):
    _name = "estate.property.offers"
    _description = "this model is used to define the offers received to the property"

    price = fields.Float()
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, ondelete="cascade")
    deadline = fields.Date(
        default=date.today(),
        copy=False,
        compute="_compute_deadline",
        readonly=False,
        # store=True,
    )
    validity_days = fields.Integer(
        default=0,
        copy=False,
        compute="_compute_validity",
        readonly=False,
        # store=True
    )

    @api.depends("validity_days")
    def _compute_deadline(self):
        for records in self:
            records.deadline = date.today() + relativedelta(days=records.validity_days)

    @api.depends("deadline")
    def _compute_validity(self):
        for records in self:
            diff = relativedelta(records.deadline, date.today())
            records.validity_days = diff.days

    # def inverse_func(self):
