from odoo import api, exceptions, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta


class Estate_Property_Type(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Types"
    active = False

    name = fields.Char(
        required=True,
        string="Type"
    )

    _sql_constraints = [
        ("check_unique_type", "UNIQUE(name)", "Property types must be unique.")
    ]


class Estate_Property_Tag(models.Model):
    _name = "estate_property_tag"
    _description = "Estate property Tags"

    name = fields.Char(
        required=True,
        string="Type"
    )

    property_estate_ids = fields.Many2many(
        "estate_property",
        string="Estate Properties"
    )

    _sql_constraints = [
        ("check_unique_tag", "UNIQUE(name)", "Property tags must be unique.")
    ]


class Estate_Property_Offer(models.Model):
    _name = "estate_property_offer"
    _description = "Estate Property Offers"

    price = fields.Float(
        string="Price"
    )

    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")],
        readonly=True,
        copy=False,
        string="Status"
    )

    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string="Partner"
    )

    property_id = fields.Many2one(
        'estate_property',
        string="Property"
    )

    validity = fields.Integer(
        default=7,
        string="Validity (days)"
    )

    deadline = fields.Date(
        compute="_compute_deadline",
        copy=False,
        string="Deadline"
    )

    _sql_constraints = [
        ("check_positive_price", "CHECK(price > 0.0)", "Offer Price should be a positive number (higher than 0).")
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.deadline = date.today() + relativedelta(days=+record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = relativedelta(date.today(), record.deadline)

    def action_accept(self):
        for record in self:
            if not any(offer_status == "accepted" for offer_status in record.property_id.offer_ids.mapped("status")):
                # Set values in the Property itself
                record.property_id.selling_price = record.price
                record.property_id.buyer = record.partner_id

                record.status = "accepted"
            else:
                raise exceptions.UserError("An offer has already been accepted.")
        return True

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                # Set values in the Property itself
                record.property_id.selling_price = 0.0
                record.property_id.buyer = None
            record.status = "refused"
        return True
