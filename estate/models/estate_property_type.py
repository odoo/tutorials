from odoo import fields,models;

class EstatePropertyType(models.Model):
      _name="estate.property.type"
      _description="type of property like home , appratemnt,row house"


      name=fields.Char(string="Property Type",required=True)
