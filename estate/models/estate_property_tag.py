from odoo import fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tags"
    _unique_tag_id = models.Constraint(
        'UNIQUE(name)',
        'This tag is alread available',
    )

    name = fields.Char(string="Name", required=True)
    _unique_tag_id = models.Constraint(
        'UNIQUE(name)',
        'This tag is alread available',
    )
