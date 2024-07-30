from odoo import models, fields


class ContainerType(models.Model):
    _name = 'container.type'
    _description = 'Container Type'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')
    container_type = fields.Selection(
        selection=[
            ('dry', 'Dry'),
            ('reefer', 'Reefer'),
            ('special', 'Special Equ.')
        ], string='Is', required=True)
    size = fields.Float(string='Size', default=0)
    volume = fields.Float(string='Volume', default=0)
    status = fields.Boolean(string='Status', default=True)
