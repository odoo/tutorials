from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offers"

    price = fields.Float(required=True)
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'An offer price must be strictly positive',
    )

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.deadline = fields.Date.add(fields.Date.to_date(record.create_date), days=record.validity)
            else:
                record.deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.deadline - fields.Date.to_date(record.create_date)).days
            else:
                record.validity = (record.deadline - fields.Date.today()).days

    def action_confirm_offer(self):
        for record in self:
            if 'accepted' in record.property_id.offer_ids.mapped('status'):
                raise UserError(self.env._("An offer has already been accepted for this property"))
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
        return True

    def action_cancel_offer(self):
        for record in self:
            record.status = 'refused'
        return True
