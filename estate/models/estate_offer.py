from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.date_utils import add
from odoo.tools.float_utils import float_compare


class EstateOffer(models.Model):
    _name = "estate.offer"
    _description = "An estate offer"

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

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    # Actions

    def set_status_accepted(self):
        for record in self:
            if (
                float_compare(record.price, record.property_id.expected_price * 0.9, 2)
                == -1
            ):
                raise ValidationError(
                    "Offer has to be at least 90% of the expected price"
                )

            for offer in self.property_id.offer_ids:
                if offer.status == "accepted":
                    raise UserError("Only one offer can be accepted")

            record.status = "accepted"

        return True

    def set_status_refused(self):
        for record in self:
            record.status = "refused"

        return True
