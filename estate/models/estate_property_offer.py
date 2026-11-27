from odoo import api, fields, models
from odoo.exceptions import UserError
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

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
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
                raise UserError(
                    self.env._("An offer has already been accepted for this property.")
                )
            if offer.property_id.state in ("sold", "canceled"):
                raise UserError(
                    self.env._("This property has already been sold or canceled.")
                )
            if offer.date_deadline < fields.Date.today():
                raise UserError(self.env._("This offer is already expired."))
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model_create_multi
    def create(self, vals_list):
        property_ids = {
            vals["property_id"] for vals in vals_list if vals.get("property_id")
        }
        properties_by_id = (
            self.env["estate.property"].browse(property_ids).grouped("id")
        )

        for vals in vals_list:
            prop = properties_by_id.get(vals.get("property_id"))
            if not prop:
                continue
            if prop.state in ("sold", "canceled", "offer_accepted"):
                raise UserError(
                    self.env._(
                        "This property has already been sold, canceled or has an accepted offer so you cannot create a new offer for it."
                    )
                )
            max_offer = max(prop.offer_ids.mapped("price"), default=0)
            if float_compare(vals.get("price", 0), max_offer, precision_digits=2) < 0:
                raise UserError(
                    self.env._("The offer must be higher than %.2f.", max_offer)
                )

        res = super().create(vals_list)
        res.property_id.filtered(lambda p: p.state == "new").state = "offer_received"
        return res
