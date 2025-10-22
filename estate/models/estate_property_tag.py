from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "ici je mets une phrase 3"
    _name_unique = models.Constraint("unique (name)", "Ce tag existe déjà.")

    name = fields.Char(required=True)
