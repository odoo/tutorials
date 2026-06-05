from odoo import fields,models

class EstateProperty(models.Model):
    _name="estate.property"
    _description="EState property"
    
    name = fields.Char(required="true")
    description=fields.Text()


