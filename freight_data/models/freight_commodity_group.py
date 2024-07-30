from odoo import fields, models


class FreightCommodityGroup(models.Model):
    _name = "freight.commodity.group"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
