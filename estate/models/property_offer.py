from odoo import api, exceptions, fields, models


class PropertyOffer (models.Model):
    _name = "estate.property.offer"
    _description = "Property Purchase Offers"

    price = fields.Float(string="Price")
    property_id = fields.Many2one("estate.property", string="Property Name", required=True)
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    status = fields.Selection(string="Status", selection=[("accepted", "Accepted"), ("refused", "Refused")], copy=False)
    validity = fields.Integer(string="Validity", default="7")
    date_deadline = fields.Date(string="Deadline", compute="_compute_validity", inverse="_inverse_date")

    @api.depends("validity")
    def _compute_validity(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_date(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_confirm(self):
        for record in self:
            if not record.status:
                if record.property_id.status in ("sold", "cancelled"):
                    raise exceptions.UserError("This offer can not be accepted")
                record.property_id.sell_apartment()
                record.status = "accepted"
                record.property_id.selling_price = record.price
                record.property_id.partner_id = record.partner_id

        return True

    def action_cancel(self):
        for record in self:
            if not record.status:
                record.status = "refused"
        return True
