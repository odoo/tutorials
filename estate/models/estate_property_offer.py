from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"
    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "An offer price must be strictly positive"),
    ]

    price = fields.Float(required=True)
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity")
    def _compute_date_deadline(self) -> None:
        for offer in self:
            offer.date_deadline = fields.Datetime.add(offer.create_date or fields.Datetime.now(), days=offer.validity)

    def _inverse_date_deadline(self) -> None:
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days

    @api.model
    def create(self, vals):
        estate_property = self.env["estate.property"].browse(vals["property_id"])

        if estate_property.state == "sold":
            raise UserError(_("You can't create offer for a property sold!"))
        if tools.float_compare(vals["price"], estate_property.best_price, 0) == -1:
            raise UserError(_("Offer with lower amount than an existing offer!"))

        estate_property.state = "offer_received"
        return super().create(vals)

    def action_offer_accepted(self) -> bool:
        self.ensure_one()
        if any(offer.status == "accepted" and offer.id != self.id for offer in self.property_id.offer_ids):
            raise UserError(_("Another property already accepted!"))
        self.status = "accepted"
        self.property_id.state = "offer_accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer_id = self.partner_id
        return True

    def action_offer_refused(self) -> bool:
        self.ensure_one()
        if self.status == "accepted":
            self.property_id.selling_price = None
            self.property_id.buyer_id = None
            self.property_id.state = "offer_received"
        self.status = "refused"
        return True
