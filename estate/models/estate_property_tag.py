from odoo import fields,models

class EsatePropertyTag(models.Model):
    _name='estate.property.tag'
    _description='Estate Property Tag'

    name=fields.Char()
