from odoo import models,fields


class EstatePropertyTyeps(models.Model):
    _name="estate.property.types"
    _description="Types of Estate Property"

    name=fields.Char(required=True)