from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string='Partner', required=True)
    property_id = fields.Many2one("estate.property", string='Property', required=True)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Date deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)',
         'Prices must be strictly positive'),
    ]

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                current_date = fields.Date.today()
                expiration_date = current_date + timedelta(days=record.validity)
                record.date_deadline = expiration_date
            else:
                record.date_deadline = fields.Date.today()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                current_date = fields.Date.today()
                validity_days = (record.date_deadline - current_date).days
                record.validity = validity_days
            else:
                record.validity = 0

    def action_accept(self):
        if not self.property_id.buyer:
            if (self.price < self.property_id.expected_price * .9):
                raise ValidationError("The selling price must be least 90% of the expected price! You must reduce the expected price if you want to accept this offer")
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer = self.partner_id
        else:
            raise UserError("Offer is already accepted")
        return True

    def action_refuse(self):
        if self.property_id.buyer == self.partner_id:
            self.property_id.buyer = ''
            self.property_id.selling_price = 0
        self.status = "refused"
        return True

    def unlink(self):
        for offer in self:
            if offer.status == 'accepted':
                offer.property_id.buyer = ''
                offer.property_id.selling_price = 0
        return super().unlink()
