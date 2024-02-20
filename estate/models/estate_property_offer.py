from odoo import fields, models, api
from odoo.exceptions import UserError


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
    partner_id = fields.Many2one("res.partner", required=True, string="Buyer")
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(
        compute="_compute_date_deadline", inverse="_compute_validity", string="Deadline"
    )

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            created_at = record.create_date or fields.Date.today()
            record.date_deadline = fields.Date.add(created_at, days=record.validity)

    def _compute_validity(self):
        for record in self:
            created_at = record.create_date or fields.Date.today()
            delta = record.date_deadline - created_at.date()
            record.validity = delta.days

    def action_confirm(self):
        for record in self:
            if record.property_id.state in ["sold", "canceled"]:
                raise UserError("Property reached a final state")
            if record.property_id.selling_price:
                raise UserError("Cannot accept more than one offer")
            record.status = "accepted"
            record.property_id.state = "offer_accepted"
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_reject(self):
        for record in self:
            if record.property_id.state in ["sold", "canceled"]:
                raise UserError("Property reached a final state")
            if record.status == "accepted":
                record.property_id.state = "offer_recieved"
                record.property_id.buyer_id = None
                record.property_id.selling_price = 0
            record.status = "refused"
        return True
