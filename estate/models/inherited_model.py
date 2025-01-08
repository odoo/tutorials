from odoo import models,fields


class InheritedModel(models.Model):
    
    _inherit= "res.users"
    
    
    property_ids = fields.One2many(
        comodel_name='estate.property',  
        inverse_name='user_id',  
        string='Properties_Inherited' , 

        )
