from odoo import fields, models


class FreightContainerType(models.Model):
    _name = "freight.container.type"
    _description = "Freight Container Type Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        ondelete='cascade'
    )
    is_options = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('special', 'Special Equ.')
    ], string="Is:", required=True)
    size = fields.Float("number", default="0.00")
    volume = fields.Float("Volume", default="0.00")
