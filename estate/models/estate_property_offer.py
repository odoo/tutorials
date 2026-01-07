from datetime import timedelta

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property offer for each property.'

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(
        compute='_compute_deadline', inverse='_inverse_deadline'
    )

    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        "The Offer price cannot be negative."
    )

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (
                    record.date_deadline - record.create_date.date()
                ).days
            else:
                record.validity = (record.date_deadline - fields.Date.today())

    def action_accepted(self):
        accepect_records = self.property_id.offer_ids.filtered(lambda o: o.status == 'accepted')
        if accepect_records:
            raise UserError("Only one offer can be accepted.")
        self.status = "accepted"
        self.property_id.partner_id = self.partner_id
        self.property_id.selling_price = self.price
        self.property_id.state = 'offer_accepted'

    def action_refused(self):
        if self.status == 'accepted':
            self.property_id.partner_id = None
            self.property_id.selling_price = None
            self.property_id.state = 'offer_received'
        self.status = "refused"

    @api.ondelete(at_uninstall=False)
    def _ondelete_offer(self):
        if self.status == 'accepted':
            raise ValidationError('Accepted offer cannot be deleted.')
