from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    deposit_id = fields.Many2one(comodel_name="product.product", string="Deposit")

    @api.model
    def get_values(self):
        res = super().get_values()
        deposit_id = self.env["ir.config_parameter"].sudo().get_param("deposit_rental.deposit_id")
        res.update(deposit_id=int(deposit_id) if deposit_id else False)
        return res

    def set_values(self):
        super().set_values()
        self.env["ir.config_parameter"].sudo().set_param("deposit_rental.deposit_id", self.deposit_id.id if self.deposit_id else False)
        self.env["product.template"].sudo()._update_deposit_amount()
