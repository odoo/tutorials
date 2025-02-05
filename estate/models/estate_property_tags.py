from odoo import fields,models;

class EstatePropertyTag(models.Model):
      _name="estate.property.tag"
      _description="Tags for Property"


      name=fields.Char(string="Property Tag",required=True)
