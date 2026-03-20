from odoo import api, fields, models
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = "An offer placed on some property"
    _order = 'price desc'

    validity = fields.Integer(string='Validity (days)', default=7)
    price = fields.Float(string='Price')
    date_deadline = fields.Date(string='Deadline', compute='_compute_deadline', inverse='_compute_validity')
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(comodel_name='estate.property.type', related='property_id.property_type_id', store=True)

    _check_price = models.Constraint('CHECK(price > 0)', 'Price must be positive')

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)

    def _compute_validity(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - fields.Date.to_date(record.create_date)).days

    @api.model_create_multi
    def create(self, vals):
        for offer in vals:
            property_id = offer.get('property_id')
            property = self.env['estate.property'].browse(property_id)

            if offer.get('price') <= max(property.mapped('best_price')):
                raise UserError("The offer price must be higher than the previous offers")

            if property.state == 'new':
                property.state = 'offer_received'
        return super().create(vals)

    def action_accept_offer(self):
        for record in self:
            if record.status == 'refused':
                raise UserError("This offer was already refused")
            if fields.Date.today() > record.date_deadline:
                raise UserError("This offer has already expired")
            if record.property_id.buyer_id:
                raise UserError("An offer has already been accepted")
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
        return True

    def action_reject_offer(self):
        for record in self:
            if record.status == 'accepted':
                raise UserError("This offer was already accepted")
            record.status = 'refused'
        return True
