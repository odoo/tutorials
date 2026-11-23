from odoo import api, fields, models
from odoo.exceptions import UserError
import datetime as dt
from odoo.tools import float_compare


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
        string="Deadline",
    )

    _check_positive_price = models.Constraint("CHECK(price > 0)", "Offer price must be strictly positive.")

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                record.date_deadline = record.create_date + dt.timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            estate_property = self.env["estate.property"].browse(vals["property_id"])
            if estate_property.state == "sold":
                raise UserError(self.env._("Cannot create an offer for a sold property."))
            if float_compare(vals["price"], max(estate_property.offer_ids.mapped("price"), default=0), 2) < 0:
                raise UserError(self.env._("Cannot create an offer with a lower amount than an existing offer."))
            else:
                estate_property.state = "offer_received"

        return super().create(vals_list)

    def action_accept(self):
        for record in self:
            other_accepted = record.property_id.offer_ids.filtered(lambda o: o.status == "accepted" and o != record)
            if other_accepted:
                raise UserError(self.env._("An offer has already been accepted for this property!"))
            record.status = "accepted"

            # TODO: check if its possible to call a method to change state on estate.property for transparency
            record.property_id.state = "offer_accepted"
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True
