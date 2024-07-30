from odoo import fields, models


class ContainerType(models.Model):
    _name = 'container.type'
    _description = 'Container Type Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
    transport_modes = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('special', 'Special Equ.')
    ], string='Is:', required=True)
    size = fields.Float(string="Size")
    volume = fields.Float(string="Volume")
    