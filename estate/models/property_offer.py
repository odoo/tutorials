from dateutil.relativedelta import relativedelta
from odoo import fields, models, api, exceptions


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'estate property offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type')

    _sql_constraints = [
        ('check_offer_price_strictly_positive', 'CHECK (price > 0)', "The offer price must be strictly positive.")]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + relativedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_confirm(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.state = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_reject(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals):
        for record in self:
            property_id = record.env['estate.property'].browse(vals['property_id'])
            if property_id.offer_ids:
                minOffer = min(property_id.offer_ids.mapped('price'))
                if vals['price'] < minOffer:
                    raise exceptions.UserError(f"The offer must be higher than {minOffer}")
        return super().create(vals)
