from odoo import api, fields, models
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer for Estate Property"
    _order = "price desc"

    price = fields.Float(
        "Price",
        required=True,
    )
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one(
        "res.partner",
        required=True,
    )
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline",
        compute="_compute_date_deadline",
        inverse="_compute_inverse_deadline",
    )
    _check_offer_price = models.Constraint(
        "CHECK (price > 0.0)",
        "Offer price must be strictly positive",
    )

    @api.model_create_multi
    def create(self, vals_list):
        if vals_list:
            property_id = self.env["estate.property"].browse(
                vals_list[0].get("property_id")
            )
            best_price = property_id.best_price

            for vals in vals_list:
                if vals["price"] < best_price:
                    raise ValidationError(
                        "Can't add this offer, price is lower than an existing offer."
                    )

            property_id.state = "offer_received"
        return super().create(vals_list)

    @api.ondelete(at_uninstall=False)
    def unlink_offer(self):

        if len(self.property_id.offer_id) == len(self):
            self.property_id.state = "new"

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = fields.Date.add(
                fields.Date.to_date(create_date), days=offer.validity
            )

    def _compute_inverse_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.validity = (
                offer.date_deadline - fields.Date.to_date(create_date)
            ).days

    def action_accept(self):
        for record in self:
            refused_offer = record.property_id.offer_id - record
            refused_offer.status = "refused"
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
