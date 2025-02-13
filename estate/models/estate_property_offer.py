from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", ondelete="restrict"
    )
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    validate = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_status = fields.Selection(related="property_id.status", store=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    
    @api.depends("validate")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = datetime.today() + relativedelta(
                days=record.validate
            )

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                delta = record.date_deadline - datetime.today().date()
                record.validate = delta.days
            else:
                record.validate = 0

    @api.constrains("price", "status")
    def _check_accepted_offer_price(self):
        for record in self:
            if (
                record.status == "accepted"
                and float_compare(
                    record.price, record.property_id.expected_price * 0.9, 2
                )
                == -1
            ):
                raise ValidationError(
                    "The accepted offer price cannot be less than 90% of the expected price!"
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_obj = self.env["estate.property"].browse(vals["property_id"])

            if vals["price"] < property_obj.best_prices:
                raise ValidationError(
                    "Offer price cannot be lower than the best offer."
                )

            property_obj.status = "offer_received"

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            record.status = "accepted"
            record.property_id.status = "offer_accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.selling_price = 0
                record.property_id.status = "offer_received"
            record.status = "refused"
