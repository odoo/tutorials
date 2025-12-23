from datetime import date

from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffers(models.Model):
    _name = "estate.property.offers"
    _description = "Real Estate Property Offers"
    _order = "price desc"

    price = fields.Float(string="Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('rejected', "Rejected")],
        copy=False,
        readonly=True,
    )
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    property_id = fields.Many2one(comodel_name='estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type', store=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            start_date = record.create_date if record.create_date else date.today()
            record.date_deadline = start_date + relativedelta(days=record.validity)

    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'accepted'
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_reject_offer(self):
        for record in self:
            record.status = 'rejected'
        return True

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError(self.env._("Offer price cannot be negative."))

    @api.model_create_multi
    def create(self, offer_list):
        for record in offer_list:
            property_id = self.env['estate.property'].browse(record['property_id'])
            if property_id.offer_ids:
                max_offer = max(property_id.offer_ids.mapped('price'))
                if record.get('price', 0) < max_offer:
                    raise UserError(self.env._("The offer must be higher than existing offers!"))
            property_id.state = 'offered'
        return super().create(offer_list)
