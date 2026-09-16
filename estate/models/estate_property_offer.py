from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'

    date_deadline = fields.Date(string='Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True)
    price = fields.Float(string='Price')
    property_id = fields.Many2one(comodel_name='estate.property', string='Property', required=True)
    status = fields.Selection(
        string='Status',
        readonly=True,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    validity = fields.Integer(string='Validity', default=7)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def accept_offer(self):
        if any(any(offer.status == 'accepted' for offer in record.property_id.offers) for record in self):
            raise UserError(_('Only one offer can be accepted by property.'))
        for record in self:
            record.status = 'accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def refuse_offer(self):
        for record in self:
            if record.status == 'accepted':
                record.property_id.buyer = None
                record.property_id.selling_price = None
            record.status = 'refused'
        return True

    def action_view_property(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'estate.property',
            'name': _('Properties'),
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', '=', self.property_id.id)],
        }
