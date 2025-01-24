from odoo import api, fields, models
from odoo.exceptions import ValidationError


class WarrantyConfiguration(models.Model):
    _name = "product.warranty.configuration"
    _description = "product.warranty.configuration"

    name = fields.Char(string="name", required=True)
    product_template_id = fields.Many2one(
        "product.template", required=True, ondelete="cascade"
    )
    percentage = fields.Float()
    years = fields.Integer(default=1)

    @api.onchange("percentage")
    def _onchange_percentage(self):
        for record in self:
            if record.percentage < 0 or record.percentage > 100:
                raise ValidationError(
                    "The value of 'Your Float Field' must be between 0 and 100."
                )
