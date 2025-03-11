from odoo import models
from odoo import Command

class InheritedModel(models.Model):
    _inherit = "estate.property"


    # Create a project for the buyer when a property is sold, with:
    #       - 
    #       - 
    def action_sold(self):
        
        
        return super().action_sold()

