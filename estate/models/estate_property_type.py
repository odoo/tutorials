from odoo import models, fields, api # type: ignore

class estatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "This is property Type table."
    _order = "sequence, name desc"

    name = fields.Char(required=True)
    _order = "name"
    active = fields.Boolean(default=True)
    number = fields.Integer(default=10)
    sequence = fields.Integer('Sequence', default=5)

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Property')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
#     tag_ids = fields.Many2many(
#         comodel_name= 'estate.property.tag',
#         relation='type_join_tag',
#         column1='type_id',
#         column2='tag_id'
#     )
    offer_count = fields.Integer(compute="_compute_offer_count")
#     tag_count = fields.Integer(compute="_compute_tag_count")

    _sql_constraints = [
            ('check_unique_type_name','UNIQUE(name)','This type is already exists.')
    ]
    
    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
                record.offer_count = len(record.offer_ids)

    @api.depends('tag_ids')
    def _compute_tag_count(self):
        for record in self:
                record.tag_count = len(record.tag_ids)




