from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare


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
    property_type_id = fields.Many2one(
        "estate.property.type", related="property_id.property_type_id", store=True
    )
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )
    validity = fields.Integer(default=7)

    _check_price = models.Constraint(
        "CHECK(price > 0)",
        "The offered price must be strictly positive.",
    )

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = (
                record.create_date or fields.Date.today()
            ) + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            creation_date = record.create_date or fields.Datetime.today()
            record.validity = (
                record.date_deadline - creation_date.date()
            ) // timedelta(days=1)

    @api.model
    def create(self, vals_list):
        for record in vals_list:
            property = self.env["estate.property"].browse(record.get("property_id"))
            if float_compare(record.get("price"), property.best_price, 2) == -1:
                raise ValidationError(
                    "A new offer price can't be lower than the best price"
                )
            property.status = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            if not record.property_id.buyer_id:
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id
            else:
                raise UserError(self.env._("The property already have a buyer defined"))

    def action_refuse(self):
        for record in self:
            record.status = "refused"
