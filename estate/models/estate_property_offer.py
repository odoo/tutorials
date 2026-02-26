from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer model"
    _order = "price desc"

    price = fields.Float("Price", required=True)
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("rejected", "Rejected")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(
        "Date Deadline",
        compute="_compute_deadline",
        inverse="_inverse_deadline",
    )
    property_type_id = fields.Many2one(
        "estate.property.type",
        string="Property Type",
        related="property_id.property_type_id",
        store=True,
    )

    _check_price = models.Constraint(
        "CHECK(price > 0)", "offer price must be greator than zero"
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for rec in self:
            curr_date = rec.create_date
            rec.date_deadline = (
                (curr_date + timedelta(days=rec.validity))
                if curr_date
                else fields.Date.today() + timedelta(days=rec.validity)
            )

    def _inverse_deadline(self):
        for rec in self:
            start_date = (
                rec.create_date.date() if rec.create_date else fields.Date.today()
            )
            rec.validity = (rec.date_deadline - start_date).days

    @api.constrains("price")
    def _check_selling_price(self):
        for rec in self:
            expected_price = rec.property_id.expected_price
            if float_is_zero(expected_price, precision_digits=2):
                continue
            min_price = expected_price * 0.9
            if float_compare(rec.price, min_price, precision_digits=2) < 0:
                raise ValidationError(
                    _("The offer price must be at least 90% of the expected price.")
                )

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_rec = self.env["estate.property"].browse(vals["property_id"])
            if property_rec.offer_ids:
                accepted_rec = property_rec.offer_ids.filtered(
                    lambda o: o.status == "accepted"
                )
                if accepted_rec:
                    raise UserError(_("offer can not be created"))
                max_offer = max(property_rec.offer_ids.mapped("price"))
                if vals.get("price") <= max_offer:
                    raise ValidationError(
                        _("offer must me greator than existing offers")
                    )
            if property_rec.state == "new":
                property_rec.state = "offer_received"
        return super().create(vals_list)

    def action_accept(self):
        if self.status == "accepted":
            raise UserError(_("offer already accepted"))
        if self.property_id.state == "cancelled":
            raise UserError(_("cancelled property cant be accepted"))
        else:
            self.property_id.offer_ids.filtered(lambda o: o.id != self.id).write(
                {"status": "rejected"}
            )
            self.property_id.write(
                {
                    "buyer_id": self.partner_id.id,
                    "selling_price": self.price,
                    "state": "offer_accepted",
                }
            )
            self.status = "accepted"
        return True

    def action_refuse(self):
        if self.status == "rejected":
            raise UserError("already refused")
        elif self.status == "accepted":
            self.property_id.selling_price = max(
                self.property_id.offer_ids.mapped("price")
            )
            self.status = "rejected"
        return True
