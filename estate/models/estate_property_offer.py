# Part of Odoo. See LICENSE file for full copyright and licensing details.

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for real estate properties"
    _order = "price desc"

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
    property_type_id = fields.Many2one(related="property_id.property_type_id", store=True)

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
            if (record.create_date):
                if (record.date_deadline):
                    record.validity = (record.date_deadline - record.create_date.date()).days

    def action_refuse(self):
        _ = self.env._
        for record in self:
            if (record.status != 'accepted'):
                record.status = 'refused'
            else:
                raise ValidationError(_("Accepted offer cannot be canceled"))
        return True

    def action_accept(self):
        _ = self.env._
        # Make sure that only one offer is selected
        self.ensure_one()

        # Accept the offer
        if self.status != 'refused':
            self.status = 'accepted'
        else:
            raise ValidationError(_("Refused offer cannot be accepted"))

        # Reject other offers
        self.property_id.offer_ids.filtered(lambda offer: offer != self).status = 'refused'

        # Set the buyer and selling price
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price
        return True

    @api.model_create_multi
    def create(self, vals_list):
        _ = self.env._
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals.get('property_id'))
            highest_offer = max(property.offer_ids.mapped('price')) if len(property.offer_ids) > 0 else 0
            offer_price = vals.get('price', 0)
            if highest_offer > offer_price:
                raise ValidationError(_("Cannot create an offer with a lower price than an existing one"))
        return super().create(vals_list)
