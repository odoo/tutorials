from odoo import api, models, fields


class VendorStatus(models.Model):
    _name = "vendor.status"
    _description = "Vendor Status"

    name = fields.Char(string="Vendor Status", required=True)
    description = fields.Char(string="Description")
    sequence = fields.Integer(string="Sequence", default=1)
    status_change_type = fields.Selection(
        selection=[
            ("any_user", "Any User"),
            ("certain_users", "Certain Users"),
            ("automatic", "Automatic"),
        ],
        string="Status Change Type",
        required=True,
        default="any_user",
        help="Define who is allowed to change the status: any user, specific users, or handled automatically.",
    )
    status_change_user_ids = fields.Many2many(
        "res.users",
        "allowed_status_id",
        string="Status Change Users",
        help="Users who can change the status",
    )
    notify_user_ids = fields.One2many(
        "res.users",
        "notify_status_id",
        string="Notify Users",
        help="Users to be notified",
    )
    prevent_po_creation = fields.Selection(
        selection=[("yes", "Yes"), ("alert", "Alert"), ("no", "No")],
        string="Prevent PO Creation",
        help="Prevent PO Creation if set to Yes or Alert",
    )

    @api.onchange("status_change_type")
    def _onchange_status_change_type(self):
        if self.status_change_type != "certain_users":
            self.status_change_user_ids = [(5, 0, 0)]
