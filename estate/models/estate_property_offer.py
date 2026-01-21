from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer Information'

    price = fields.Float(string='Price')
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(start_date, days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            start_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - start_date).days

    def action_accept_offer(self):
        for record in self:
            if "accepted" in record.property_id.offer_ids.mapped('status'):
                raise UserError("An offer has already been accepted for this property.")
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.property_id.buyer_id = record.partner_id

    def action_refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("You cannot refuse an accepted offer.")
            record.status = 'refused'
