from datetime import datetime, timedelta

from odoo import _, api, exceptions, fields, models
from odoo.tools.float_utils import float_compare


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "Test description for estate.property.offer model"
    _order = 'price DESC'

    price = fields.Float()
    status = fields.Selection(
        string="Offer Status",
        copy=False,
        selection=[('accepted', "Accepted"), ('refused', "Refused")])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)

    _check_price = models.Constraint(
        'CHECK (price > 0)',
        "The price must be strictly positive",
    )

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            # record.create_date is "falsy" so if checking with `record.create_date if hasattr(record.create_date) else datetime.today()` then it's true because it hasattr but it's None so it's converted to false
            record.date_deadline = ((record.create_date or datetime.today()) + timedelta(days=record.validity)).date()

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    @api.constrains('price')
    def _check_selling_price_90_percent(self):
        for record in self:
            if float_compare(record.price, 0.9 * record.property_id.expected_price, precision_digits=2) == -1:
                raise exceptions.UserError(_("The selling price cannot be lower than 90% of the expected price"))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            property = self.env['estate.property'].browse(vals['property_id'])
            property.state = 'offer_received'
        return super().create(vals_list)

    @api.depends('property_id', 'property_id.offer_ids')
    def action_offer_accept(self):
        for record in self:
            if any(o.status == 'accepted' for o in record.property_id.offer_ids):
                raise exceptions.UserError(_("Cannot accept more than one offer"))
            if float_compare(record.price, 0.9 * record.property_id.expected_price, precision_digits=2) == -1:
                raise exceptions.UserError(_("The selling price cannot be lower than 90% of the expected price"))
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price

    def action_offer_refuse(self):
        self.status = 'refused'  # assigns the same value to all the records
