from odoo import api, fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type, i.e. type of the building accourding to the use"
    _order = "sequence, name"

    property_ids = fields.One2many('estate.property', 'property_type_id', string='Property')
    offer_ids = fields.One2many(
                'estate.property.offer',
                'property_type_id')
    
    name = fields.Char(required=True)
    _check_name = models.Constraint(
            'unique (name)',
            'The property type name must be unique, choose different name')
    description = fields.Text(help="Description of thus estate property type for better user understanding")
    code = fields.Char(required=True, help="Single to double character code for identification when space is scarce")
    _check_code = models.Constraint(
            'unique (code)',
            'The property type code must be unique, choose different code')
    sequence = fields.Integer(default=1, help="Ordering sequence, ower is first")
    offer_count = fields.Integer(
            'Amount of offers',
            compute='_compute_offer_count',
            help='Computed field with amount of the offers related to this type')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
