from odoo import models, fields


class PropertyTypeTags(models.Model):

    # ---------------------------------------- Private Attributes ---------------------------------
    _name = 'estate.property.tags'
    _description = 'Estate Property Tags'
    _order = 'name'

    # --------------------------------------- Fields Declaration ----------------------------------

    name = fields.Char(required=True)
    color = fields.Integer()
