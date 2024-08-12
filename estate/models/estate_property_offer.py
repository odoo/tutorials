from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Property Offer'
    _order = 'price desc'

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string="Status", copy=False)
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")
    property_id = fields.Many2one('estate.property', 'Property', required=True, ondelete="cascade")
    property_type_id = fields.Many2one(related="property_id.property_type_id")

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = fields.Date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                create_date_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date_date).days
            else:
                record.validity = 0

    def action_accept(self):
        if not self.property_id.buyer_id:
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer_id = self.partner_id
            self.property_id.state = "offer_accepted"
        else:
            raise UserError("Offer has been already Accepted")
        return True

    def action_refuse(self):
        if self.property_id.buyer_id == self.partner_id:
            self.property_id.buyer_id = ''
            self.property_id.selling_price = 0
        self.status = 'refused'
        return True

    _sql_constraints = [
        ('check_offer_price', 'CHECK(price > 0)', 'The offer price must be strictly positive.')
    ]

    @api.model
    def create(self, vals):
        record = super().create(vals)
        if record.property_id.state == 'new':
            record.property_id.state = 'offer_received'
        if record.price < max(record.property_id.offer_ids.mapped('price')):
            raise UserError("Price should be greater than the existing offer")
        return record
