from odoo import fields, models


class FreightPackageType(models.Model):
    _name = "freight.package.type"
    _description = "Freight Package Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        ondelete='cascade'
    )
    is_options = fields.Many2many(
        comodel_name="package.type.options",
        string="Is:",
        required=True
    )
