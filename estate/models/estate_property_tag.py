from odoo import models, fields # type: ignore

class estatePropertyTag(models.Model):
    
    _name = "estate.property.tag"
    _description = "This is property Tag model"

    name = fields.Char(required=True, string="Tag")
    active = fields.Boolean(required=True)
    # property_ids = fields.Many2many(
    #             comodel_name='estate.property',
    #             string='Properrrrty',
    #             relation='property_join_tag',
    #             column1='property_id',
    #             column2='tag_id'
    #     )
    property_ids = fields.Many2many(
        comodel_name='estate.property',
        string='properties'
    )