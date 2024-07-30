from odoo import models, fields


class FreightContainerType(models.Model):
    _name = "freight.container.type"
    _description = "this is freight Container type"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    is_option = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('special_equ', 'Special Equ')
    ],
    string='Is:',
    default='dry'
    )
    size = fields.Float(string="Size", default=0.00)
    volume = fields.Float(string="Volume", default=0.00)
    status = fields.Boolean(string='Status', default=True)
