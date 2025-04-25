import math

from dateutil import relativedelta

from odoo import _, api, exceptions, fields, models


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property Offer'
    _order = 'price desc'

    price = fields.Float(string='Price')
    status = fields.Selection(selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (days)', default=7)
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(
        string='Property Type',
        related='property_id.property_type_id',
        store=True,
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'The price must be strictly positive.'),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        properties = {
            p.id: p
            for p in self.env['estate.property'].browse([
                e.get('property_id') for e in vals_list if e.get('property_id')
            ])
        }

        for vals in vals_list:
            property = properties.get(vals.get('property_id'), '')

            if not properties or 'price' not in vals:
                continue

            if vals['price'] < min([*property.offer_ids.mapped('price'), math.inf]) and len(property.offer_ids) > 1:
                raise exceptions.UserError(_('An offer cannot have a lower price then an existing offer.'))

            if property.state == 'new':
                property.write({'state': 'received'})

        return super().create(vals_list)

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.write({'date_deadline': create_date + relativedelta.relativedelta(days=record.validity)})

    def _inverse_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.write({'validity': (record.date_deadline - create_date.date()).days})

    def action_refuse_offer(self):
        for record in self:
            record.write({'status': 'refused'})
        return True

    def action_accept_offer(self):
        for record in self:
            record.write({'status': 'accepted'})
            record._onchange_status()

        return True

    @api.onchange('status')
    def _onchange_status(self):
        if self.status != 'accepted':
            return

        if self.property_id.state in {'accepted', 'sold'}:
            self.write({'status': False})
            raise exceptions.UserError(_('An offer as already been accepted.'))

        self.property_id.write({
            'selling_price': self.price,
            'state': 'accepted',
            'partner_id': self.partner_id,
        })
