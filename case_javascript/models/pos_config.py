from odoo import fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    congratulatory_text = fields.Char(
        string='Congratulatory Text',
        default='Congratulations!')
