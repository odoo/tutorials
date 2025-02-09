from odoo import fields,models,api
from datetime import timedelta

class EstatePropertytOffer(models.Model):
    _name = "estate.property.offer"
    _description ="It defines the estate property Offer"

    price= fields.Float(copy=False, string='Price')
    status= fields.Selection(selection=[('Accepted','Accepted'), ('Refused','Refused')], string='Status', copy=False)
    partner_id= fields.Many2one('res.partner', string="Partner", required=True)
    property_id= fields.Many2one('estate.property', string='Property',required=True)
    validity= fields.Integer(default=7)
    date_deadline= fields.Date(compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.create_date=record.create_date or fields.Datetime.today()
            record.date_deadline= record.create_date.date() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.create_date= record.create_date or fields.Datetime.today()
            record.validity=(record.date_deadline-record.create_date.date()).days
