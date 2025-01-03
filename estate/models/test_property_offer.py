from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import models,fields,api


class test_property_offer(models.Model):
    _name = "test.property.offer"

    price = fields.Float('price',required=True)
    status = fields.Selection([('Accepted','Accepted'),('Refused','Refused'),('Pennding','pennding')],default="Pennding",copy=False)
    buyer_id = fields.Many2one('res.partner',string='partner_id',required=True)   
    property_id = fields.Many2one('test.property',required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_date_deadline',inverse='_inverse_date_deadline',default=datetime.today())

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self: 
            record.date_deadline = (datetime.today() +relativedelta(days = record.validity)).date()


    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity =  (record.date_deadline - datetime.today().date()).days
            else:
                record.date_deadline = 0
    

            









