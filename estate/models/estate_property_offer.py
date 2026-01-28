from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstateProperOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer."
    _order = "price desc"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Deadline')
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.type_id')

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    @api.depends('create_date', 'validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=+record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=+record.validity)

    def _inverse_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept(self):
        if self.status != 'accepted':
            for offer in self.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise UserError(_('Only one offer can be accepted.'))
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.state = 'offer_accepted'
        return True

    def action_refuse(self):
        self.status = 'refused'
        if self.property_id.state != 'offer_accepted':
            self.property_id.selling_price = None
            self.property_id.state = 'offer_received'
        return True

    @api.model
    def create(self, vals_list):
        for vals in vals_list:
            property_id = self.env['estate.property'].browse(vals['property_id'])
            max_offer = 0
            if property_id.offer_ids:
                max_offer = max(offer for offer in property_id.offer_ids).price
            if vals['price'] > max_offer:
                self.env['estate.property'].browse(vals['property_id']).state = 'offer_received'
            else:
                raise UserError(_("You cannot add an offer with a price lower than the maximum existing price."))
        return super().create(vals_list)
