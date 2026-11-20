from odoo import fields, models


class EstateAssignTypeWizard(models.TransientModel):
    _name = "estate.assign.type.wizard"
    _description = "Assign type to property"
    _rec_name = 'property_type_id'

    property_type_id = fields.Many2one(
        'estate.property.type', string="Type", readonly=True
    )
    property_ids = fields.Many2many('estate.property')

    def action_assign_type(self):
        self.property_ids.property_type_id = self.property_type_id
