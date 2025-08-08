from odoo import models, api


class InheritedPosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _load_pos_data_models(self, config_id):
        data_models = super()._load_pos_data_models(self.config_id.id)
        data_models.append('hr.employee')
        return data_models
