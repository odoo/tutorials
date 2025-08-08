from odoo import fields, models


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    # Boolean field to enable or disable the 'Put In Pack' feature for this picking type
    put_in_pack_toggle = fields.Boolean(
        string="Put In Pack"
    )

class Picking(models.Model):
    _inherit = "stock.picking"

    # Related field to get the 'Put In Pack' setting from the associated picking type
    put_in_pack_toggle = fields.Boolean(
        related="picking_type_id.put_in_pack_toggle"
    )
