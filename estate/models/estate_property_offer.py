from odoo import models, fields, api
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.tools.float_utils import float_compare
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"
    price = fields.Float()
    property_id = fields.Many2one("estate.property", ondelete="restrict")
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
    property_status=fields.Selection(related="property_id.status", store=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )  #!This field is for stat button

    #! used model create multi because @api.model is deprecated
    @api.model_create_multi  # sets property state as offer received on creation also prevents creation of offers lower than current one
    def create(self, vals_list):
        print(vals_list)
        for vals in vals_list:
            if vals["property_id"]:
                prop = self.env["estate.property"].browse(vals["property_id"])
                if vals["price"] < prop.best_offer:
                    raise ValidationError("Offer price cannot be lower than best offer")
                if prop.status == "new":
                    prop.status = "offer_received"
                elif prop.status == "offer_accepted":
                    raise ValidationError("Offer already accepted for this property")

        return super().create(vals_list)

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
            if record.property_id.status == "offer_received":
                record.status = "accepted"
                record.property_id.status = "offer_accepted"
                record.property_id.selling_price = self.price
                record.property_id.buyer_id = record.partner_id
            else:
                if record.property_id.status == "sold":
                    raise ValidationError("Property already sold")
                elif record.property_id.status == "offer_accepted":
                    raise ValidationError("Offer already accepted")
                else:
                    raise ValidationError("Property canceled")

    def action_refuse(self):
        for record in self:
            if record.property_id.status == "offer_received":
                record.status = "refused"
                record.property_id.selling_price = 0
            elif record.property_id.status == "sold":
                raise ValidationError("Property already sold")
            elif record.property_id.status == "offer_accepted":
                raise ValidationError("Offer already accepted")
            else:
                raise ValidationError("Property canceled")

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
