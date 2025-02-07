from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'

    price = fields.Float(string="Offer Price", required=True)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status"
    )
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    create_date = fields.Datetime('Creation Date', readonly=True, default=fields.Datetime.now)
    validity = fields.Integer('Validity (in days)', default=7)
    date_deadline = fields.Date('Date Deadline', compute='_compute_date_deadline')

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = (record.create_date + timedelta(days=record.validity)).date()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = (record.date_deadline - record.create_date.date()).days

    def action_accept_offer(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("This property is already sold!")
            if record.property_id.buyer_id:
                raise UserError("This property already has a buyer!")
            record.status = 'accepted'
            record.property_id.buyer_id = record.partner_id
            record.property_id.selling_price = record.price
            record.property_id.state = 'sold'
            
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
            record.property_id.state = 'not sold'
            record.property_id.buyer_id = False
            record.property_id.selling_price = False

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]


