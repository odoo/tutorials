from odoo import models, fields


class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    modular_type_id = fields.Many2one(
        'modular.type.config',
        string='Modular Type',
        help="The modular type configuration for this BOM line."
    )
