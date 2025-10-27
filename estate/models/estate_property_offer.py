from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    _order = "price DESC"

    price = fields.Float()
    status = fields.Selection(
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Buyer",  required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_type_id = fields.Many2one("estate.property.type", related="property_id.property_type_id", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state not in ("accepted", "sold", "cancelled"):
                record.property_id.state = "accepted"
                record.status = "accepted"
                record.property_id.selling_price = self.price
                record.property_id.buyer_id = self.partner_id
            else:
                raise UserError(_("This offer can't be accepted because the property is currently %s.")% record.property_id.state)
        return True

    def action_refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                record.property_id.state = "new"
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = ""
            record.status = "refused"
        return True

    _positive_offer_price = models.Constraint(
        "CHECK(price > 0)",
        "The offer price must be strictly positive.",
    )
