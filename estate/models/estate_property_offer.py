from odoo.exceptions import UserError

from odoo import api, fields, models
from odoo.tools.float_utils import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Offer Description"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)")
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            base_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.date_deadline = fields.Date.add(base_date, days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            base_date = (
                offer.create_date.date() if offer.create_date else fields.Date.today()
            )
            offer.validity = (offer.date_deadline - base_date).days

    def action_accept(self):
        for offer in self:
            if "accepted" in offer.property_id.offer_ids.mapped("status"):
                raise UserError("An offer has already been accepted for this property.")
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            prop = self.env["estate.property"].browse(vals["property_id"])
            if prop.offer_ids:
                max_offer = max(prop.mapped("offer_ids.price"))
                if float_compare(vals["price"], max_offer, precision_digits=2) < 0:
                    raise UserError(f"The offer must be higher than {max_offer:.2f}.")
                elif prop.state == "sold":
                    raise UserError(
                        "This property has already been sold so you cannot create a new offer for it."
                    )
            prop.state = "offer_received"
        return super().create(vals_list)
