from dateutil.relativedelta import relativedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_date")
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _check_offer_price = models.Constraint(
        "CHECK(price > 0)", "An offer price must be strictly positive"
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            default_creation_date = record.create_date or fields.Date.today()
            record.date_deadline = (
                relativedelta(days=record.validity) + default_creation_date
            )

    def _inverse_date(self):
        for record in self:
            default_creation_date = record.create_date or fields.Date.today()
            record.validity = (
                record.date_deadline - fields.Date.to_date(default_creation_date)
            ).days

    @api.model
    def create(self, vals):
        if len(vals) > 0:
            property_ids = [val.get("property_id") for val in vals]
            properties = self.env["estate.property"].browse(property_ids)
            properties_map = {prop.id: prop for prop in properties}
        for record in vals:
            prop = properties_map.get(record.get("property_id"))
            if prop.state == "new":
                prop.state = "offer_received"
            if record["price"] < prop.best_price:
                raise UserError(_("Cannot create an offer with a lower amount than an existing offer."))
        return super().create(vals)

    def action_accept(self):
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.customer = self.partner_id
        self.property_id.state = "offer_accepted"
        self.property_id.offer_ids.filtered(
            lambda record: not record.status
        ).write({"status": "refused"})
        return True

    def action_refuse(self):
        self.status = "refused"
        self.property_id.customer = None
        return True
