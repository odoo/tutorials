from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', required=True, string="Property")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.date_deadline = create_date.date() + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.validity = (offer.date_deadline - create_date.date()).days if offer.date_deadline else 0

    def action_set_accept(self):
        for record in self:
            if (record.property_id.state in ('offer accepted', 'sold')):
                raise UserError('An offer already accepted for this property')
            if (record.property_id.state == 'canceled'):
                raise UserError('Property canceled')
            if (record.status in ('refused', 'accepted')):
                raise UserError('Offer already accepted/refused')

            record.property_id.selling_price = record.price
            record.property_id.state = 'offer accepted'
            record.property_id.buyer_id = record.partner_id
            record.status = 'accepted'
        return True

    def action_set_refuse(self):
        for record in self:
            if (record.property_id.state in ('offer accepted', 'sold')):
                raise UserError('An offer already accepted for this property')
            if (record.property_id.state == 'canceled'):
                raise UserError('Property canceled')
            if (record.status in ('accepted', 'refused')):
                raise UserError('Offer already accepted/refused')
            record.status = 'refused'
        return True
