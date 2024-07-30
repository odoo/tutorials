from odoo import fields, models


class FreightServiceScope(models.Model):
    _name = "freight.service.scope"
    _description = "Freight Service Scope Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        required=True,
        ondelete='cascade'
    )
    description = fields.Text("Description")
