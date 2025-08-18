from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    allowed_status_id = fields.Many2one(
        "vendor.status",
        string="Allowed Vendor Status",
        help="The vendor status this user is allowed to change",
    )
    notify_status_id = fields.Many2one(
        "vendor.status",
        string="Notify on Vendor Status",
        help="Notify this user when the selected vendor status is applied",
    )
