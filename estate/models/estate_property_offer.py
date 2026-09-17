from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Price')
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], copy=False, string='Status')
    validity = fields.Integer(string='Validity (Days)', default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline', string='Deadline')
    partner_id = fields.Many2one('res.partner', required=True, string='Partner')
    property_id = fields.Many2one('estate.property', required=True)

#   Constraints:
    _check_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price should be stricty positive'
    )

#   computed fields

    @api.depends('validity', 'create_date')
    def _compute_date_deadline(self):
        for record in self:
            base_date = record.create_date or fields.Date.today()  # Fallback when create_date is not set yet:
            record.date_deadline = fields.Date.add(base_date, days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

#   Action buttons

    def action_accept_property_offer(self):
        for record in self:
            for properties in record.property_id:
                properties.action_set_selling_offer(record.partner_id, record.price)
            record.status = 'accepted'
            return True
        return True

    def action_refuse_property_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError('Accepted offer cannot be refused !')
            record.status = 'refused'
            return True
        return True
