from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "ici je mets une phrase 2"
    _name_unique = models.Constraint("unique (name)", "Ce type de propriété existe déjà.")

    name = fields.Char(required=True)
