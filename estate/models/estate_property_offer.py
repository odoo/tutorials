from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import date_utils


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real-estate property offer"
    _order = "price desc"

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            _("The offer price must be strictly positive."),
        )
    ]

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for offer in self.filtered("create_date"):
            offer.date_deadline = date_utils.add(offer.create_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            offer.validity = date_utils.relativedelta(
                offer.date_deadline, offer.create_date
            ).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            offer_property = self.env["estate.property"].browse(vals["property_id"])
            if offer_property.state == "new":
                offer_property.state = "offer_received"

            if offer_property.offer_ids and vals["price"] < max(
                offer_property.offer_ids.mapped("price")
            ):
                raise UserError(
                    _("New offers must have a higher value than previous offers.")
                )

        return super().create(vals_list)

    def action_accept(self):
        for offer in self:
            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True
