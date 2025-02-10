from odoo import models,fields,api

class EstatePropertyOffer(models.Model):
    _name="estate.property.offer"
    _description="Real Estate Property Offer Model"

    price=fields.Float(required=True,copy=False,default=0)
    status=fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')],copy=False)
    partner_id=fields.Many2one('res.partner',required=True)
    property_id=fields.Many2one('estate.property',required=True)
    validity=fields.Integer(string="Validity (in days)",default=7)
    date_deadline=fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline',string="Deadline")

    @api.depends('create_date','validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline=fields.Date().add(record.create_date.date(),days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity=(record.date_deadline-record.create_date.date()).days
