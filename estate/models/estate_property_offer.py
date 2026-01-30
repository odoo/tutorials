from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float("Price")
    state = fields.Selection(
        string="Status",
        copy=False,
        readonly=True,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_compute_validity")

    property_id = fields.Many2one("estate.property", string="Property", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(creation_date, days=record.validity)

    def _compute_validity(self):
        for record in self:
            creation_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - creation_date.date()).days

    @api.model
    def create(self, vals):
        for record in vals:
            property = self.env["estate.property"].browse(record["property_id"])
            if record["price"] < property.best_offer:
                raise UserError(f"The offer must be above {property.best_offer}")
            property._set_offer_received()

        return super().create(vals)

    def action_accept(self):
        self.ensure_one()
        self.state = "accepted"

        property = self.property_id
        property.selling_price = self.price
        property.partner_id = self.partner_id

        if property.state == "offer_received":
            property.state = "offer_accepted"

        for offer in property.offer_ids:
            if offer.id != self.id:
                offer.state = "refused"

        return True

    def action_refuse(self):
        for record in self:
            record.state = "refused"

        property = self.property_id

        if "accepted" not in property.offer_ids.mapped("state"):
            property.state = "offer_received"

        property.selling_price = None
        property.partner_id = None

        return True
