from datetime import date, timedelta

from odoo import api, fields, models

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted','Accepted'),
            ('refused','Refused'),
        ],
    )
    validity = fields.Integer(default=7, string="Validity (days)")
    date_deadline = fields.Date(compute='_compute_deadline', inverse='_inverse_deadline', string="Deadline")
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)
    
    @api.depends('validity','property_id.create_date')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = timedelta(days=record.validity) + record.property_id.create_date or date.today()
    
    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline and record.property_id.create_date:
                record.validity = (record.date_deadline - record.property_id.create_date.date()).days
            else:
                record.validity = 0
    
    def action_accept_offer(self):
        for record in self:
            record.status = 'accepted'
            record.property_id.selling_price = record.price
            record.property_id.partner_id = record.partner_id
        return True
    
    def action_refuse_offer(self):
        for record in self:
            record.status = 'refused'
        return True

    _sql_constraints = [
        ('check_offer_price','CHECK(price > 0)','The offer price must be strictly positive'),
    ]    
