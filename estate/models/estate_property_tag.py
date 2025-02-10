from odoo import fields,models

class EstatePropertyType(models.Model):
    _name="estate.property.tag"
    _description="Estate Property Tag"

#------------------------------------------------Basic Fields-------------------------------------------#
    name=fields.Char(required=True,string="Name")

