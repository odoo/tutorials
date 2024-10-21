from datetime import timedelta
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"

    _sql_constraints = [
        (
            "check_positive_offer_price",
            "CHECK(price > 0)",
            "The offer price must be strictly positive.",
        ),
    ]
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validiy (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = create_date.date() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.validity = (offer.date_deadline - create_date.date()).days

    def action_accept_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError(_("You already accepted the offer."))
            if offer.property_id.buyer_id:
                raise UserError(_("Only one offer can be accepted."))
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            for property_offer in offer.property_id.offer_ids:
                if property_offer.id != offer.id:
                    offer.status = "refused"
        return True

    def action_refuse_offer(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError(
                    _("You cannot refuse an offer once it has been accepted.")
                )
            offer.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env["estate.property"].browse(vals["property_id"])
            price = vals["price"]
            if any(prev_offer.price > price for prev_offer in property_id.offer_ids):
                raise UserError(_("An offer with an higher price already exists."))
            property_id.state = "offer_received"
        return super().create(vals_list)
