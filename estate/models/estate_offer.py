from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "An estate offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    validity = fields.Integer(default=7)

    # Foreign fields
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    # Computed fields
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    # Related fields
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    # Constraints
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Offer price must be stricly positive",
    )

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = add(
                record.create_date if record.create_date else fields.Date.today(),
                days=+record.validity,
            )

    @api.onchange("date_deadline")
    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    # Actions

    def action_status_accepted(self):
        self.ensure_one()

        if self.status in ("accepted", "refused"):
            raise UserError("The state of an offer cannot be changed once it is set")

        if float_compare(self.price, self.property_id.expected_price * 0.9, 2) == -1:
            raise ValidationError("Offer has to be at least 90% of the expected price")

        if any(
            self.property_id.offer_ids.filtered(
                lambda offer: offer.status == "accepted"
            )
        ):
            raise UserError("Only one offer can be accepted")

        self.property_id.state = "accepted"
        self.status = "accepted"

        for offer in self.property_id.offer_ids:
            if offer.id == self.id:
                continue

            offer.status = "refused"

        return True

    def action_status_refused(self):
        self.ensure_one()

        if self.status in ["accepted", "refused"]:
            raise UserError("The state of an offer cannot be changed once it is set")

        self.status = "refused"
        return True

    # Overwrites

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env["estate.property"].browse(vals["property_id"])
            if property.state == "sold":
                raise UserError("No offer can be made for a sold property")

            if property.state == "new":
                property.state = "received"

        return super().create(vals_list)
