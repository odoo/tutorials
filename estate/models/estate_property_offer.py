from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False,
    )
    validity = fields.Integer("Validity (days)", default=7)

    # Many2one references
    partner_id = fields.Many2one(comodel_name="res.partner", required=True)
    property_id = fields.Many2one(comodel_name="estate.property", required=True)
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type", related="property_id.type_id", store=True
    )

    # Computed fields
    date_deadline = fields.Date(
        string="Deadline Date",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = base_date + timedelta(days=record.validity)

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            if record.date_deadline and base_date:
                record.validity = (record.date_deadline - base_date).days

    def action_confirm_offer(self):
        self.ensure_one()
        # Check property have already been sold or canceled
        if self.property_id.state in ["sold", "canceled"]:
            raise UserError(
                self.env._("This property has already been sold or canceled!")
            )

        # Any accepted offer?
        if any(o.status == "accepted" for o in self.property_id.offer_ids):
            raise UserError(self.env._("An offer have already been accepted!"))

        # Accept offer
        self.status = "accepted"
        self.property_id.write(
            {
                "state": "offer_accepted",
                "selling_price": self.price,
                "buyer_id": self.partner_id.id,
            }
        )

    def action_refuse_offer(self):
        for offer in self:
            offer.status = "refused"

    _check_price = models.Constraint("CHECK(price >= 0)", "Offer price must be >= 0!")

    # Model decorators
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property_rec = self.env["estate.property"].browse(vals["property_id"])

            for offer in property_rec.offer_ids:
                if vals.get("price", 0) <= offer.price:
                    raise UserError(
                        self.env._(
                            "The offer amount must be strictly higher than existing offers."
                        )
                    )

            property_rec.state = "offer_received"

        return super().create(vals_list)
