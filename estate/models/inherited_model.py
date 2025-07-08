from odoo import  fields,models

class InheritedFields(models.Model):
    _inherit= 'res.users'

    property_ids = fields.One2many('estate.property','salesman_id',domain=[('state','not in',['sold','cancelled'])])