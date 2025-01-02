from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    property_id = fields.Many2one("estate.property", required=True)
    partner_id = fields.Many2one("res.partner", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        default=datetime.today(),
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + relativedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - datetime.today().date()
                record.validity = delta.days
            else:
                record.validity = 0

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = self.price

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.selling_price = 0

    @api.constrains("price", "status")
    def _check_accepted_offer_price(self):
        for record in self:
            if (
                record.status == "accepted"
                and float_compare(record.price, record.property_id.expected_price, 2)
                == -1
            ):
                raise ValidationError(
                    "The accepted offer price cannot be less than 90% of the expected price!"
                )
