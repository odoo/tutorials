from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyBooking(models.Model):
    _name = "estate.property.booking"
    _description = "Property Booking"

    name = fields.Char("Booking", required=True, readonly=True, default="New")
    property_id = fields.Many2one('estate.property', required=True)
    buyer_id = fields.Many2one('res.partner', "Buyer", required=True)
    final_price = fields.Float(related="property_id.selling_price")
    booking_amount = fields.Float(compute="_compute_amounts", store=True)
    remaining_amount = fields.Float(compute="_compute_amounts", store=True)
    state = fields.Selection([
        ("draft", "Draft"),
        ("booked", "Booked"),
        ("paid", "Paid")
    ], default="draft")

    @api.depends("property_id.selling_price")
    def _compute_amounts(self):
        for rec in self:
            rec.booking_amount = rec.final_price * 0.10
            rec.remaining_amount = rec.final_price - rec.booking_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    "estate.booking.sequence") or "New"
        return super().create(vals_list)

    def action_book(self):
        self.ensure_one()
        self.state = "booked"
        self.property_id.state = "booked"

    def action_pay(self):
        self.ensure_one()
        payment = self.env["estate.property.payment"].create({
            "booking_id": self.id,
            "amount": self.remaining_amount,
        })
        return {
            "type": "ir.actions.act_window",
            "name": "Payment",
            "res_model": "estate.property.payment",
            "view_mode": "form",
            "res_id": payment.id,
            "target": "new",
        }
