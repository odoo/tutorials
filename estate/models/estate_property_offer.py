from datetime import date

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.translate import _


class EstateProperOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer."

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string='Deadline')

    ## CONSTRAINTS ##

    _check_offer_price = models.Constraint(
        'CHECK(price > 0)',
        'The offer price must be strictly positive.',
    )

    ## COMPUTE FUNCTIONS ##

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

    ## ACTIONS ##

    def action_accept(self):
        if self.status != 'accepted':
            for offer in self.property_id.offer_ids:
                if offer.status == 'accepted':
                    raise UserError(_('Only one offer can be accepted.'))
            self.status = 'accepted'
            self.property_id.selling_price = self.price
        return True

    def action_refuse(self):
        if self.status == 'accepted':
            self.status = 'refused'
            self.property_id.selling_price = None
        return True
