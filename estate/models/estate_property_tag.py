from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate_property_tag_model"
    _order = "name"

    name = fields.Char(required=True)
    property_ids = fields.Many2many(
        comodel_name="estate_property_model",
        relation="estate_property_tag_rel",
        column1="estate_property_tag_id",
        column2="estate_property_id",
        string="Properties"
    )