from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline", string="Deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.create_date or fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.selling_price != 0.0 and record.status != 'accepted':
                raise exceptions.UserError("Pay attention: in real life only one offer can be accepted for a given property!")
            else:
                record.status = 'accepted'
                record.property_id.selling_price = record.price
                record.property_id.buyer_id = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.selling_price = 0.0
                record.property_id.buyer_id = None
            record.status = 'refused'
