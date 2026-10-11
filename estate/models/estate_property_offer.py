from odoo import fields, models, api


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer for Estate Property"

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
    type_id = fields.Many2one("estate.property.type")
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
            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price

            refused_offer = record.property_id.property_offer_id - record
            for offer in refused_offer:
                offer.status = "refused"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
