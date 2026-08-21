from odoo import models, fields


class EstatePropertyTags(models.Model):
    _name = "estate.property.tags"
    _description = "Estate Property Tags"
    _order = "name"
    name = fields.Char(string="Name", required=True)
    property_id = fields.Many2one(
        comodel_name="estate.property",
        string="Property",
    )
    color = fields.Integer()
    _check_tag_name = models.Constraint(
        "UNIQUE(name)", "Property tag name must be unique."
    )
