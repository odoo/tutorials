import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError
from odoo.tools import float_utils


class PropertyOffer(models.Model):
    # Private attributes
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    # Field declarations
    create_date = fields.Date(default=lambda self: datetime.date.today())
    price = fields.Float()
    status = fields.Selection(
        [
            ("proposed", "Proposed"),
            ("accepted", "Accepted"),
            ("refused", "Refused"),
        ],
        default="proposed",
        copy=False,
    )
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    actions_visible = fields.Boolean(compute="_compute_actions_visible")
    property_type_id = fields.Many2one(
        related="property_id.type_id", comodel_name="estate.property.type"
    )

    # SQL constraints and indexes
    _check_price = models.Constraint(
        "CHECK(price > 0)", "The price should be positive."
    )

    # Compute, inverse and search methods
    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            create_date = (
                record.create_date if record.create_date else datetime.date.today()
            )
            record.deadline = create_date + datetime.timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            create_date = (
                record.create_date if record.create_date else datetime.date.today()
            )
            record.validity = (record.deadline - create_date).days

    @api.depends("property_id.state")
    def _compute_actions_visible(self):
        for record in self:
            record.actions_visible = (
                record.property_id.state not in ["sold", "offer_accepted", "cancelled"]
                and record.status == "proposed"
            )

    # Constrains methods and onchange methods
    # CRUD methods
    def create(self, vals):
        properties = self.env["estate.property"].browse(record["property_id"] for record in vals)

        if any(properties.mapped(lambda x: x.state in ["sold", "offer_accepted", "cancelled"])):
            raise AccessError("You cannot create an offer on a sold/cancelled property or when there\'s already an offer accepted.")

        for property, record in zip(properties, vals):
            best_price = float(max(property.offer_ids.mapped("price"), default=0.0))

            if "price" not in record or float_utils.float_compare(float(record["price"]), best_price, precision_digits=2) < 0:
                raise UserError("You cannot go under the price of the current best offer")

            property.state = "offer_received"

        return super().create(vals)

    def write(self, vals):
        if "price" in vals:
            for record in self:
                best_price = float(max(record.property_id.offer_ids.mapped("price"), default=0.0))

                if float_utils.float_compare(float(vals["price"]), best_price, precision_digits=2) < 0:
                    raise UserError("You cannot go under the price of the current best offer")

                if record.property_id.state not in ["sold", "cancelled"]:
                    record.property_id.state = "offer_received"
                else:
                    raise AccessError("You cannot create an offer on a sold or cancelled property.")

        return super().write(vals)

    # Action methods
    def action_accept(self):
        for record in self:
            if record.status == "refused" or record.property_id.state in ['cancelled', 'sold']:
                raise UserError("Can\'t accept a refused offer or accept an offer on a sold/cancelled property.")

            if float_utils.float_compare(record.price, record.property_id.expected_price, precision_digits=2) < 0:
                raise UserError("You can\'t buy below the expected price")

            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.status == "accepted" or record.property_id.state in ["cancelled", "sold"]:
                raise UserError("Can\'t refuse an accepted offer or refuse an offer on a sold/cancelled property.")
            record.status = "refused"
