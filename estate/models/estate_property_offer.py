from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one(
        "estate.property", string="Property", ondelete="restrict"
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        store=True,
        string="Deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        related="property_id.property_type_id",
        string="Property Type",
        store=True,
    )

    _price_check = models.Constraint(
        "CHECK(price >= 0)", "The offer price must be greater then 0"
    )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = vals.get("property_id")
            property_record = self.env["estate.property"].browse(property_id)
            property_record.state = "offer_received"

            existing_offers = property_record.offer_ids.mapped("price")

            if existing_offers and vals.get("price") <= max(existing_offers):
                raise UserError(
                    "Offer price must be greater than existing offers price !!"
                )

        return super().create(vals_list)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()
            record.date_deadline = base_date + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days

    def action_accept(self):
        for record in self:
            record.property_id.buyer_id = record.partner_id
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.selling_price = record.price

            other_offers = record.property_id.offer_ids.filtered(
                lambda offers: offers.id != record.id
            )

            other_offers.write({"status": "refused"})
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("You cannot refuse an accepted offer.")
            record.status = "refused"
        return True
