from odoo import api, fields, models
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real estate offers"
    _order = "price desc"

    property_id = fields.Many2one(
        "estate.property", string="Property", required=True, ondelete="cascade"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )
    price = fields.Float(string="Price", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline"
    )
    partner_id = fields.Many2one("res.partner", string="Partner", copy=False)
    status = fields.Selection(
        string="Status",
        selection=[
            ("pending", "Pending"),
            ("refused", "Refused"),
            ("accepted", "Accepted"),
        ],
        required=True,
        copy=False,
        default="pending",
    )

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price >= 0)",
            "Offer price must be positive.",
        ),
        (
            "check_partner",
            "CHECK(partner_id != NULL)",
            "Who made this offer ?",
        ),
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        """
        This function calculates the deadline based on the create date and validity period for each record.
        """
        for record in self:
            record.deadline = (
                record.create_date.date() if record.create_date else fields.Date.today()
            ) + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        """
        This function calculates the number of days between a record's deadline and either its creation date
        or the current date if the creation date is not available.
        """
        for record in self:
            record.validity = int(
                (
                    record.deadline
                    - (
                        record.create_date.date()
                        if hasattr(record, "create_date")
                        else fields.Date.today()
                    )
                ).days
            )

    @api.constrains("price")
    def _offer_price_constrain(self):
        """
        The function `_offer_price_constrain` checks if any offer price is higher than the property price
        and raises a validation error if so.
        """
        for offer in self.property_id.offer_ids:
            if offer.price > self.price:
                raise ValidationError(
                    f"A higher offer has already been set at {offer.price}€."
                )

    @api.constrains("status")
    def _offer_validation_constrain(self):
        """
        The function `_offer_validation_constrain` validates and processes an offer within a property,
        ensuring only one offer is accepted at a time.
        """
        if self.status == "accepted":
            for offer in self.property_id.offer_ids:
                if offer != self and offer.status == "accepted":
                    raise ValidationError("Another offer has already been accepted.")

            for order_to_refuse in self.property_id.offer_ids:
                if order_to_refuse != self:
                    order_to_refuse.status = "refused"

            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.status = "offer_accepted"

    def action_accept_offer(self):
        """
        The function `action_accept_offer` sets the status attribute to "accepted" and returns True.
        :return: The method `action_accept_offer` is returning a boolean value `True`.
        """
        self.status = "accepted"
        return True

    def action_reject_offer(self):
        """
        The function `action_reject_offer` sets the status attribute to "refused" and returns True.
        :return: The method `action_reject_offer` is returning a boolean value `True`.
        """
        self.status = "refused"
        return True
