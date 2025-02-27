from odoo import models

class ProductTemplate(models.Model):
    _inherit = "product.template"

    def action_update_quantity_on_hand(self):
        """Override this method to prevent the 'Update Quantity' action from executing."""
        return False  # This stops the action from running
