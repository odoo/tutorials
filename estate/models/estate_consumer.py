from odoo import fields, models,api  # type: ignore
from datetime import timedelta, datetime
from odoo.exceptions import ValidationError # type: ignore

class EstateConsumerModel(models.Model):

    _name = "estate.consumer"
    _description = "Estate Consumer Model"
    
    name = fields.Char()
    email = fields.Char()
    contact = fields.Integer()

    # Action Name = 'False'
    def action_anonymous(self):
        return False
    
    # Action Name = 'String'
    def action_string(self):
        return 'action_anonymous'
    
    # Action name = 'Number'
    def action_number(self):
        return self.env.ref('estate.estate_property_action').id
    
    # Action name = 'Dictionary'
    def action_dict(self):
         # Return a dictionary to open the form view of the canceled property
        return {
        'type': 'ir.actions.act_window',
        'name': 'Canceled Property',
        'res_model': 'estate.consumer',
        'view_mode': 'form',
        'res_id': self.id,  # The ID of the current record
        'target': 'new',
        }
    