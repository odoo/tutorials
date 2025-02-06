from odoo import fields, models

class estatePropertyTag(models.Model):
  _name = "estate.property.tag"
  _description = "Estate property Tag"

  name = fields.Char(required=True)