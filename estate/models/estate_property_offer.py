from dateutil.relativedelta import relativedelta

from odoo import models, fields, api, exceptions, _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_id = fields.Many2one(
        "estate.property",
        required=True,
    )
    validity = fields.Integer(
        default=7,
    )
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    _offer_price = models.Constraint(
        "CHECK (price > 0)",
        "Offer price must be greater than 0",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for rec in self:
            create = rec.create_date or fields.Date.today()
            rec.date_deadline = (create + relativedelta(days=rec.validity))

    def _inverse_date_deadline(self):
        for rec in self:
            create = rec.create_date or fields.Date.today()
            rec.validity = (rec.date_deadline - fields.Date.today(create)).days

    def action_accept(self):
        for offer in self:
            if offer.property_id.buyer_id:
                raise exceptions.UserError(_("Only one offer can be accepted for a property."))
            offer.status = "accepted"
            offer.property_id.selling_price = offer.price
            offer.property_id.buyer_id = offer.partner_id
            offer.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for offer in self:
            offer.status = "refused"
        return True

    @api.model
    def create(self, vals):
        for rec in vals:
            property_id = rec.get("property_id")
            price = rec.get("price", 0.0)
            if property_id:
                property_obj = self.env["estate.property"].browse(property_id)
                best_offer = property_obj.best_price or 0.0
                if price < best_offer:
                    raise exceptions.UserError(_(
                        "Offer price must be greater than or equal to the best offer price."))
                property_obj.state = "offer_received"
        return super().create(vals)

