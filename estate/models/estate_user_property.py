from odoo import fields, models  # ty: ignore[unresolved-import]


class EstateUser(models.Model):
    _inherit = "res.users"  # noqa: RUF012

    property_ids = fields.One2many("estate.property", "salesman")
