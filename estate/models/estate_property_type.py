from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Loại bất động Sản"

    name = fields.Char(string="Title", required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    sequence = fields.Integer("Sequence", default=1)
    _order = "sequence, name"

    _sql_constraints = [
    ('unique_type_name', 'UNIQUE(name)', 'Tên loại không được trùng')
]
