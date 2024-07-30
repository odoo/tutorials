from odoo import fields, models


class ContainerType(models.Model):
    _name = 'container.type'
    _description = 'Container Type'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    is_type = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('special', 'Special Equ.')
    ], string='Type', required=True)
    size = fields.Float('Size', default=0.00)
    volume = fields.Float('Volume', default=0.00)
    status = fields.Boolean('Active', default=True)
