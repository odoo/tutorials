from odoo import api, models


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _load_pos_data_models(self, config_id):
        list = super()._load_pos_data_models(config_id)
        return [*list, "hr.employee"]
