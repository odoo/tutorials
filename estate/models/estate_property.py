from odoo import models, fields

class EstateProperty(models.Model):
    _name = "test_model"
    _description = "Test Model"
    name = fields.Char(name ='table')

    
    


