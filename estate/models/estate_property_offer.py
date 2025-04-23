# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, exceptions
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for real estate properties"

    price = fields.Float('Price', required=True)
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=True,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    _sql_constraints = [
        ('positive_price', 'CHECK(price > 0)', 'The price must be strictly positive.'),
    ]


    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            if (record.create_date):
                record.date_deadline = record.create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if (record.create_date & record.date_deadline):
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_refuse(self):
        for record in self:
            if (record.status != 'accepted'):
                record.status = 'refused'
            else:
                raise exceptions.ValidationError("Accepted offer cannot be canceled")
        return True

    def action_accept(self):
        # Make sure that only one offer is selected
        if (len(self) > 1):
            raise exceptions.ValidationError("Only one offer can be accepted")

        # Accept the offer
        if (self.status != 'refused'):
            self.status = 'accepted'
        else:
            raise exceptions.ValidationError("Refused offer cannot be accepted")

        # Reject other offers
        for record in self.property_id.offer_ids:
            if (record != self):
                record.status = 'refused'

        # Set the buyer and selling price
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        return True
