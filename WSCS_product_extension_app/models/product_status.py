from odoo import models, fields


class ProductStatus(models.Model):
    _name = "product.status"
    _description = "Product Status"
    _order = "sequence"

    name = fields.Char(string="Product Status", required=True)
    sequence = fields.Integer(string="Sequence", default=1)
    status_change_up_group_id = fields.Many2one(
        "res.groups", string="Status Change Up Groups"
    )
    status_change_down_group_id = fields.Many2one(
        "res.groups", string="Status Change Down Groups"
    )
