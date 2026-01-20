from odoo import api, models

class PosOrder(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config_id):
        """
        Override to include `hr.employee` in POS data models for salesperson selection.
        """
        models = super()._load_pos_data_models(config_id)
        models.append('hr.employee')
        return models
        