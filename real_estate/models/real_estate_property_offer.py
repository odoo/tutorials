from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers on Buy or Sell for properties"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ("refused", "Refused"),
            ("accepted", "Accepted"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )

    _offer_partner_uniq = models.Constraint(
        "UNIQUE(partner_id, property_id)",
        "You have already made an offer on this property",
    )

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(start_date)
            ).days

    @api.constrains("price")
    def _check_offer_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError(_("Offer Price Must be Positive"))

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id"):
                property_record = self.env["estate.property"].browse(
                    vals["property_id"]
                )
                if property_record.offer_ids:
                    max_offer = max(property_record.offer_ids.mapped("price"))
                    if vals["price"] < max_offer:
                        raise UserError(
                            _(
                                "You have to make offer higher then %(amount).2f",
                                amount=max_offer,
                            )
                        )
                property_record.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            if record.status == "accepted":
                continue
            if record.property_id.buyer_id:
                raise UserError(_("You can accept offer only once per property"))
        record.status = "accepted"
        record.property_id.buyer_id = record.partner_id
        record.property_id.selling_price = record.price
        (record.property_id.offer_ids - record).status = "refused"
        record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
            record.property_id.state = "offer_received"
            record.property_id.buyer_id = False
            record.property_id.selling_price = 0.00
        return True
