from datetime import timedelta
from odoo import models, fields, api, exceptions, _


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Offer to buy the property'
    _order = 'price desc'

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
    property_type_id = fields.Many2one(related='property_id.property_type_id')

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be greater than 0'
    )

    @api.depends('validity')
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
            if record.property_id.buyer:
                raise exceptions.UserError(_('An another offer is already accepted'))
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
            record.property_id.offer_ids.filtered(lambda x: x.id != record.id).status = "refused"
        return True

    def action_offer_refused(self):
        for record in self:
            record.status = 'refused'
        return True

    @api.model
    def create(self, vals_list):
        if len(vals_list) > 0:
            prop = self.env['estate_property'].browse(vals_list[0]['property_id'])
            if prop.best_price > vals_list[0]['price']:
                raise exceptions.UserError(_('An offer with high price already exists.'))

            prop.state = 'offer_received'

        return super().create(vals_list)

    def _cron_auto_refuse(self):
        domain = [
            ("status", "=", False),
        ]
        records = self.search(domain, limit=100)
        for record in records:
            rect = record.date_deadline
            now = fields.Date.today()
            if (rect - now) < timedelta(days=1):
                record.status = "refused"
