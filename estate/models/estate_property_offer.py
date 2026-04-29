from odoo import api, fields, models
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, ValidationError
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        [("accepted", "Accepted"), ("refused", "Refused")], copy=False
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.type_id", store=True)
    validity = fields.Integer("Validity (days)", default=7)
    date_deadline = fields.Date(
        "Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline"
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "An offer price must be stricly positive",
    )

    @api.depends("validity", "create_date")
    def _compute_date_deadline(self):
        for record in self:
            date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = date + relativedelta(days=record.validity)

    @api.model
    def create(self, vals_list):
        property = self.env["estate.property"].browse(vals_list[0]["property_id"])
        if max(property.offer_ids.mapped("price"), default=0.0) > vals_list[0]["price"]:
            raise UserError("New offer must be higher than existing ones.")

        property.state = "offer_received"

        return super().create(vals_list)

    def _inverse_date_deadline(self):
        for record in self:
            days = record.date_deadline - record.create_date.date()
            record.validity = days.days

    def action_accept(self):
        for record in self:
            property_id = record.property_id
            if property_id.state in ("sold", "accepted"):
                raise UserError("A sold or cancelled property can't be sold.")

            if (property_id.has_garden and property_id.garden_orientation == "south" and float_compare(record.price, property_id.expected_price, precision_digits=2) == -1):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")

            record.status = "accepted"
            property_id.state = "sold"
            property_id.buyer_id = record.partner_id
            property_id.selling_price = record.price

    def action_refuse(self):
        self.status = "refused"
