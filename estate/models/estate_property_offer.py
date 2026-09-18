from odoo import api, models, fields, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute="_compute_deadline", inverse="_inverse_deadline"
    )

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for record in self:
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if not record.date_deadline:
                continue
            base_date = (
                record.create_date.date() if record.create_date else fields.Date.today()
            )
            record.validity = (record.date_deadline - base_date).days

    def action_confirm(self):
        for record in self:
            if (
                record.property_id.state == "sold"
                or record.property_id.state == "cancelled"
            ):
                raise UserError(_("Property already sold, or cancelled"))
            elif record.property_id.action_sell_to_offer(
                offer_buyer_id=record.partner_id, offer_selling_price=record.price
            ):
                record.status = "accepted"

    def action_refuse(self):
        for record in self:
            record.status = "refused"
