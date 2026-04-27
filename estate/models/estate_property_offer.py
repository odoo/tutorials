import datetime


from odoo import models, fields, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

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

    _check_price = models.Constraint(
        "CHECK(price > 0)", "The price should be positive."
    )

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

    @api.model
    def write(self, vals):
        super().write(vals)
        for record in self:
            if record.property_id.state not in ["sold", "cancelled"]:
                record.property_id.state = "offer_received" if record.status != "accepted" else "offer_accepted"

    def action_accept(self):
        for record in self:
            if record.status == "refused":
                raise UserError("A refused offer cannot be accepted")
            if record.property_id.state == "cancelled":
                raise UserError("An offer on a cancelled property cannot be accepted")
            if record.property_id.state == "sold":
                raise UserError("An offer on a sold property cannot be accepted")

            record.status = "accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = "offer_accepted"

    def action_refuse(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("An accepted offer cannot be refused")
            if record.property_id.state == "cancelled":
                raise UserError("An offer on a cancelled property cannot be refused")
            if record.property_id.state == "sold":
                raise UserError("An offer on a sold property cannot be refused")

            record.status = "refused"
