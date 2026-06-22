from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer on a property"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True,
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for property_offer in self:
            property_offer.date_deadline = fields.Date.today() + relativedelta(
                days=property_offer.validity,
            )

    def _inverse_date_deadline(self):
        for property_offer in self:
            delta = property_offer.date_deadline - fields.Date.today()
            property_offer.validity = delta.days

    def accept_offer(self):
        for property_offer in self:
            if property_offer.property_id.state in ["new", "offer_received"]:
                property_offer.property_id.state = "offer_accepted"
                property_offer.property_id.buyer_id = property_offer.partner_id
                property_offer.property_id.selling_price = property_offer.price
                property_offer.status = "accepted"
            else:
                raise UserError(
                    self.env._(
                        "Cannot accept offer for already sold or cancelled property",
                    ),
                )
        return True

    def refuse_offer(self):
        for property_offer in self:
            if property_offer.status == "accepted":
                raise UserError(self.env._("Cannot refuse already accepted offer"))
            if property_offer.property_id.state in ["new", "offer_received"]:
                property_offer.status = "refused"
        return True

    @api.model
    def create(self, vals_list):
        property_ids = [vals["property_id"] for vals in vals_list]
        properties = self.env["estate.property"].browse(property_ids)

        for vals in vals_list:
            property = properties.browse(vals["property_id"])
            if property and (vals["price"] < property.best_price):
                raise UserError(self.env._("Offer must be higher than best price"))

        properties.write({"state": "offer_received"})
        return super().create(vals_list)
