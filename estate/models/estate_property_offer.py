from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for the property"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        copy=False
    )

    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True
    )
    property_id = fields.Many2one(
        "estate.property", string="Property", required=True
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        "Deadline date",
        compute="_compute_deadline_date",
        inverse="_inverse_deadline_date",
    )

    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True,
    )

    @api.depends("validity", "create_date")
    def _compute_deadline_date(self):
        for record in self:
            valifity_offset = relativedelta(days=record.validity)
            creation_date = record.create_date.date() \
                if record.create_date else fields.Date.today()
            record.date_deadline = creation_date + valifity_offset

    def _inverse_deadline_date(self):
        for record in self:
            creation_date = record.create_date.date() \
                if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - creation_date).days

    def action_accept_offer(self):
        for record in self:
            # check if there is already an accepted offer
            exists_accepted_offer = record.search_count(
                [
                    ("property_id.id", "=", record.property_id.id),
                    ("status", "=", "accepted")
                ],
                1
            )
            if exists_accepted_offer:
                raise UserError("You cannot accept multiple offers")

            # Ensure offers for estates with south-facing gardens can only be accepted if above expected price.
            if record.property_id.garden_orientation == 'south' and \
                    record.price <= record.property_id.expected_price:
                raise ValidationError(
                    "If garden orientation is south, price must be higher than expected one")

            # accept the offer
            record.status = "accepted"
            record.property_id.state = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "received"
                record.property_id.selling_price = 0
                record.property_id.buyer_id = None
            record.status = "refused"
        return True

    # Make sure that price is positive
    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "Expected price must be positive"
    )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            # raise error if creating offer with lower price
            exists_higher_offer = self.search_count(
                [
                    ("property_id.id", "=", vals["property_id"]),
                    ("price", ">", vals["price"])
                ],
                1
            )
            if exists_higher_offer:
                raise UserError("Can't create an offer with a lower price")

            # change status to received
            current_property = self.env["estate.property"].browse(
                vals["property_id"])
            current_property.state = "received"

        return super().create(vals_list)
