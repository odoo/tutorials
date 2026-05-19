from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer made on properties"
    _order = "price desc"

    property_type_id = fields.Many2one(related="property_id.property_type_id")
    price = fields.Float()
    status = fields.Selection(
        string="status",
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        help="Offer Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_compute_validity",
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be positive.",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (
                offer.create_date or fields.Date.today()
            ) + relativedelta(days=offer.validity)

    def action_accept_offer(self):
        for offer in self:
            is_not_actionable = any(
                status == "accepted"
                for status in offer.property_id.offer_ids.mapped("status")
            )
            if is_not_actionable:
                raise UserError(
                    _("An offer has already been accepted for this property."),
                )

            offer.status = "accepted"
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.selling_price = offer.price
            offer.property_id.state = "sold"

    def action_reject_offer(self):
        self.status = "refused"
        return True

    @api.depends("create_date", "date_deadline")
    def _compute_validity(self):
        for offer in self:
            offer.validity = (
                offer.date_deadline - (offer.create_date or fields.Date.today()).date()
            ).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.state == "new":
                property.state = "offer_received"

        return super().create(vals_list)
