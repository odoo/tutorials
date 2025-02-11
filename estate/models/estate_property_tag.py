from odoo import fields,models # type: ignore

class EstatePropertyType(models.Model):
    _name="estate.property.tag"
    _description="Estate Property Tag"
    _sql_constraints = [
        ('check_unique_property_tag', 'UNIQUE(name)', 'Property Tag already exists')
    ]
#------------------------------------------------Basic Fields-------------------------------------------#
    name=fields.Char(required=True,string="Name")

