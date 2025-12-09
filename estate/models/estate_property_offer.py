from odoo import models, fields, api, exceptions


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer to buy the property'

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate_property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_offer_date_deadline', inverse='_inverse_offer_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_offer_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date.date(), days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    def _inverse_offer_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accepted(self):
        for record in self:
            if record.status == 'accepted':
                return False
            if record.property_id.buyer:
                raise exceptions.UserError('An another offer is already accepted')
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.status = 'accepted'
        return True

    def action_offer_refused(self):
        for record in self:
            record.status = 'refused'
        return True
