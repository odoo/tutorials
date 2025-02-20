from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for real estate properties"
    _order = "price desc"

    price = fields.Float(required=True)
    status = fields.Selection(
        [
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer(
        string="Validity (days)",
        default=7,
        help="Validity of the offer in days",
    )
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.createdate:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        for offer in self:
            for other_offer in offer.property_id.offer_ids:
                if other_offer.status == "accepted" and other_offer.id != offer.id:
                    raise UserError("Another offer is already accepted on this property.")
        for offer in self:
            offer.status = "accepted"
            offer.property_id.state = "offer_accepted"
            offer.property_id.buyer_id = offer.partner_id.id
            offer.property_id.selling_price = offer.price
        return True

    def action_refuse(self):
        self.status = "refused"
        return True

    @api.model
    def create(self, vals):
        property_id = vals.get("property_id")
        self.env["estate.property"].browse(property_id).state = "offer_received"
        return super().create(vals)

    _sql_constraints = [
        ("check_price_positive", "CHECK(price > 0)", "The price must be strictly positive."),
    ]
