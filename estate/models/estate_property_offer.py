from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offers"
    _order = "price desc"

    price = fields.Float(string="Price", required=True)
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        string="Status",
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property")
    validate = fields.Integer(string="Validity(days)", default=7)
    date_deadline = fields.Date(
        string="Deadline", compute="_compute_deadline", inverse="_update_validity"
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        ("check_price", "CHECK(price > 0)", "Offer Price must be positive"),
    ]

    # Function of implementing comptue field and inverse function on validity days and date dadeline
    @api.depends("validate", "create_date")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date.date() + relativedelta(
                    days=record.validate
                )
            else:
                record.date_deadline = fields.Date.today() + relativedelta(
                    days=record.validate
                )

    def _update_validity(self):
        for offer in self:
            if offer.date_deadline:
                offer.validate = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validate = 7

    # Function to perform action when offer accpeted
    def action_accept(self):
        for record in self:
            if record.status == "accepted":
                raise exceptions.UserError("This property has already accepted offer!")

            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id

            record.status = "accepted"
            record.property_id.state = "offer_accepted"

            other_offers = self.search(
                [
                    ("property_id", "=", record.property_id.id),
                    ("id", "!=", record.id),
                    ("status", "=", ""),
                ]
            )

            other_offers.write({"status": "refused"})

    # Function to perform action when offer refused
    def action_refuse(self):
        for record in self:
            record.status = "refused"

    @api.model
    def create(self, vals):
        """
        Overrides the create method to enforce business rules:
        1. Prevents creating an offer lower than the highest existing offer for the same property.
        2. Updates the property state to 'Offer Received' when an offer is created.
        """
        property = self.env["estate.property"].browse(vals["property_id"])
        max_price = max(property.offer_ids.mapped("price"), default=0)
        if vals.get("price") < max_price:
            raise exceptions.UserError(f"The offer must be higher than {max_price}.")

        if property.state == "new":
            property.state = "offer_received"

        return super(EstatePropertyOffer, self).create(vals)
