from odoo import api, _, exceptions, fields, models
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "realestate.properties.offer"
    _description = "Real estate property offer"
    _order = "price desc"

    price = fields.Float("Price", required=True)
    _check_selling_price = models.Constraint(
        "CHECK(price > 0)",
        _("The price should be strictly positive"),
    )

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    validity = fields.Integer(
        "Validaty (days)",
        default=7,
    )
    date_deadline = fields.Date(
        "Deadline",
        compute="_computed_date_deadline",
        inverse="_inverse_validity_period",
        readonly=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("realestate.properties", required=True)
    property_type_id = fields.Many2one(
        "realestate.properties.type",
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("create_date", "validity")
    def _computed_date_deadline(self):
        for offer in self:
            create_date = fields.Date.to_date(offer.create_date) or fields.Date.today()
            if offer.validity:
                offer.date_deadline = fields.Date.add(
                    create_date,
                    days=offer.validity,
                )

    def _inverse_validity_period(self):
        for offer in self:
            create_date = fields.Date.to_date(offer.create_date) or fields.Date.today()
            offer.validity = (offer.date_deadline - create_date).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise exceptions.UserError(_("One offer has already been accepted."))
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
            if offer.property_id.state == "offer_received" and any(
                s != "refused" for s in offer.mapped("status")
            ):
                offer.property_id.state = "new"
            offer.property_id.selling_price = 0
            offer.property_id.buyer_id = None

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("property_id"):
                property_record = self.env["realestate.properties"].browse(
                    vals["property_id"],
                )
                offer_price = vals.get("price", 0.0)
                if (
                    property_record.best_offer
                    and float_compare(offer_price, property_record.best_offer, 2) < 0
                ):
                    raise exceptions.UserError(
                        _("New offer should be better than current best offer (%.2f).")
                        % property_record.best_offer,
                    )
                if property_record.state == "new":
                    property_record.state = "offer_received"
        return super().create(vals_list)
