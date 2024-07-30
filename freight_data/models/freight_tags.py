from odoo import fields, models


class FreightTags(models.Model):
    _name = "freight.tags"
    _description = "Freight Tags Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
