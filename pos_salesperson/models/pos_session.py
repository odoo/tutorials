from odoo import models


class PosSession(models.Model):
    _inherit = "pos.session"

    def _load_pos_data_models(self, config_id):
        models = super()._load_pos_data_models(config_id)
        models += ["hr.employee"]
        return models
