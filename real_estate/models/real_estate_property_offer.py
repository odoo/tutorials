from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers on Buy or Sell for properties"

    price = fields.Float()
    status = fields.Selection(
        [
            ("refused", "Refused"),
            ("accepted", "Accepted"),
        ],
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start_date = record.create_date or fields.Date.today()
            record.validity = (record.date_deadline - fields.Date.to_date(start_date)).days

    def action_accept(self):
        for record in self:
            if record.property_id.buyer_id:
                raise UserError("You can accept offer only once per property")
        record.status = 'accepted'
        record.property_id.buyer_id = record.partner_id
        record.property_id.selling_price = record.price
        (record.property_id.offer_ids - record).status = 'refused'
        return True

    def action_refuse(self):
        for record in self:
            record.status = 'refused'
        return True
