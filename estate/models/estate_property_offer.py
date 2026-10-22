from odoo import api, exceptions, fields, models
from odoo.tools import _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection([("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True, readonly=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _check_offer_price = models.Constraint(
        'CHECK(price >= 0)',
        'The offer price must be greater than zero (0)',
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                record.create_date or fields.Date.today(),
                days=record.validity,
            )

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        estate_property = self.property_id

        if estate_property.offer_ids.filtered(lambda offer: offer.status == "accepted"):
            raise exceptions.UserError(_("This property already has an accepted offer."))

        self.status = "accepted"
        estate_property.state = "offer_accepted"

        estate_property.buyer_id = self.partner_id
        estate_property.selling_price = self.price
        estate_property.seller_id = self.env.user

    def action_refuse_offer(self):
        for record in self:
            record.status = "refused"

    @api.model_create_multi
    def create(self, vals_list):

        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])

            if vals["price"] < property.best_price:
                raise exceptions.UserError(
                    _("You cannot create an offer lower than an existing offer.")
                )

            property.state = "offer_received"

        return super().create(vals_list)
