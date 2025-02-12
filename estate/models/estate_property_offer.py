from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate property offer'
    _order = 'price desc'

    price = fields.Float(string="price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
        ],string='Status', copy=False)
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    validity = fields.Integer(string='Validity (Days)', default=7)
    deadline_date = fields.Date(string='Deadline', compute='_compute_deadline_date', inverse='_inverse_deadline_date')        
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends('create_date', 'validity')
    def _compute_deadline_date(self):
        for record in self:
            record.deadline_date = fields.Date.add((record.create_date or fields.Date.today()), days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            record.validity = (record.deadline_date - record.create_date.date()).days if record.deadline_date else 0

    def action_order_accepted(self):
        for record in self:
            if record.property_id.state == 'offer_accepted':
                raise ValidationError("You can't accept more than 1 offer.")
            record.status = 'accepted'
            record.property_id.state = 'offer_accepted'
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    def action_order_refused(self):
        for record in self:
            record.status = 'refused'

    @api.model_create_multi
    def create(self, vals):
        for record in vals:
            property_id = self.env['estate.property'].browse(record['property_id'])
            if property_id:
                property_id.write({'state' : 'offer_received'})

            if property_id.best_offer > record['price']:
                raise UserError("Offer Price entered is lower than the existing offer price.")
        return super().create(vals)
