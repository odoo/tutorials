from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offre d'achat"
    _order = "price desc"

    price = fields.Float("price")
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    date_deadline = fields.Date(default=fields.Date.today() + relativedelta(days=7), compute="_compute_deadline", inverse="_update_validity")
    validity = fields.Integer(default=7)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    _sql_constraints = [
        ("positive_offer_price", "CHECK(price > 0)", "Offer should have a strictly positive price !")
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                now = record.create_date
                record.date_deadline = now + relativedelta(days=record.validity)

    def _update_validity(self):
        for offer in self:
            if offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days

    def action_confirm(self):
        for offer in self:

            for other_offer in offer.property_id.offer_ids:
                if other_offer.status == "accepted":
                    offer.status = "refused"

            if offer.status == "refused":
                raise UserError("Offer already refused")

            offer.status = "accepted"
            offer.property_id.buyer = offer.partner_id
            offer.property_id.selling_price = offer.price
            for other_offer in offer.property_id.mapped("offer_ids"):
                if other_offer.id != offer.id:
                    other_offer.status = "refused"
        return True

    def action_cancel(self):
        for offer in self:
            if offer.status == "accepted":
                raise UserError("Offer already accepted")
            offer.status = "refused"
        return True

    @api.model
    def create_multi(self, vals):
        property_id = self.env["estate.property"].browse(vals["property_id"])
        if property_id.state == "new":
            property_id.state = "offer received"
        if property_id.best_price > vals["price"]:
            raise UserError("The price of a new offer can't be below the price of an already existing offer.")
        return super().create_multi(vals)
