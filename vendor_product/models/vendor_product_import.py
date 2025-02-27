from odoo import exceptions, fields, models


class VendorProductImport(models.Model):
    _name = 'vendor.product.import'

    name = fields.Char(string="Name", default="New", readonly="1")
    vendor_id = fields.Many2one(comodel_name='res.partner', string="Vendor", required=True)
    vendor_template = fields.Many2one(comodel_name="vendor.product.template", string="Vendor Template Formate")
    fiel_to_process = fields.Binary(string="File to Process")
    date = fields.Datetime(string="Date")
    state = fields.Selection(
        selection=[
            ('pending', "Pending"),
            ('processed', "Processed"),
            ('error', "error")
        ],
        string="State",
        default='pending'
    )

    # Acction methods

    def action_reset_to_pending(self):
        breakpoint()
        self.state = 'pending'

    def action_manual_process(self):
        if not self.fiel_to_process:
            raise exceptions.UserError("")

