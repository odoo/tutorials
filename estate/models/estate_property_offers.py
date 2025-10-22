from odoo import api, fields, models
from odoo.exceptions import UserError


class PropertyOfferModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused")
        ],
        copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    _check_price = models.Constraint(
        "CHECK(price >= 0)",
        "The price of the offer must be positive."
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add((record.create_date or fields.Datetime.now()), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days if record.date_deadline else record.validity

    def action_accept_offer(self):
        self.ensure_one()
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id
        self.property_id.state = "accepted"
        self.refuse_all_other_offers()

    def refuse_all_other_offers(self):
        for offer in self.property_id.offer_ids:
            if offer != self:
                offer.status = "refused"

    def action_refuse_offer(self):
        self.ensure_one()
        self.status = "refused"

    @api.model
    def create(self, vals_list: list[dict]):
        for val in vals_list:
            estate_property = self.env["estate.property"].browse(val["property_id"])
            if any(offer.price > val["price"] for offer in estate_property.offer_ids):
                raise UserError("Cannot create a new offer with a lower price than an existing offer.")
            if estate_property.state == 'new':
                estate_property.state = 'received'
        return super().create(vals_list)
