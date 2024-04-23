from datetime import timedelta

from odoo import api, fields, models  # type: ignore
from odoo.exceptions import UserError, ValidationError  # type: ignore


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
        string="Status",
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(
        related="property_id.estate_property_type_id", store=True
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity", "date_deadline")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(
                    days=record.validity
                )
            else:
                record.date_deadline = fields.Date.today() + timedelta(
                    days=record.validity
                )

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days

    def action_accepted(self):
        if "accepted" in self.property_id.offer_ids.mapped("status"):
            raise UserError("Cannot accept this offer, another offer has been accepted")
        self.status = "accepted"
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id.name
        self.property_id.state = "offer accepted"
        return True

    def action_refused(self):
        self.status = "refused"
        return True

    @api.model
    def create(self, vals):
        property_id = self.env["estate.property"].browse(vals["property_id"])
        if vals["price"] < property_id.best_price:
            raise ValidationError(
                "Cannot create offer with a lower amount than an existing offer."
            )
        property_id.state = "offer received"
        return super().create(vals)

    @api.constrains("price")
    def _check_positif(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("Expected price must be positif")
