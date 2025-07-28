from dateutil import relativedelta

from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import float_utils


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "This is the model for estate property's offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    property_type_id = fields.Many2one('estate.property.type', related="property_id.property_type_id")
    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'Offer price must be positive.'),
    ]

    @api.depends('create_date', 'validity')
    def _compute_deadline_date(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta.relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta.relativedelta(days=record.validity)

    @api.depends('create_date', 'date_deadline')
    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days

    def action_offer_accept(self):
        if float_utils.float_is_zero(self.property_id.selling_price, 1):
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
        else:
            raise UserError("You already accepted an offer for this property")

    def action_offer_refuse(self):
        if not self.status:
            self.status = 'refused'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            current_property = self.env['estate.property'].browse(vals['property_id'])
            if current_property.status == 'new':
                current_property.status = 'offer_received'
            if (vals['price'] < current_property.best_price):
                raise UserError("This property already has better offers")
        return super().create(vals_list)
