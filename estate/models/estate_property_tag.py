from odoo import models, fields # type: ignore

class estatePropertyTag(models.Model):
    
    _name = "estate.property.tag"
    _description = "This is property Tag model"
    _order = "name"

    name = fields.Char(required=True, string="Tag")
    active = fields.Boolean(required=True)
    # property_ids = fields.Many2many(
    #             comodel_name='estate.property',
    #             string='Properrrrty',
    #             relation='property_join_tag',
    #             column1='property_id',
    #             column2='tag_id'
    #     )
    # property_ids = fields.Many2many(
    #     comodel_name='estate.property',
    #     string='properties'
    # )

    # property_type_id = 

    color = fields.Integer(default=12)
    _sql_constraints = [
            ('check_unique_tag_name','UNIQUE(name)','This tag is already exists.')
    ]