from odoo import api, models, fields


class FreightContainer(models.Model):
    _name = "freight.container"
    _description = "this is freight Containers"

    container_number = fields.Char(
        string='Container Number',
        required=True
    )
    container_type_id = fields.Many2one('freight.container.type', string='Container Type')
    container_owner_id = fields.Many2one('res.partner', string='Container Owner')

    @api.constrains('container_number')
    def _check_container_number(self):
        for record in self:
            if len(record.container_number) != 11:
                raise ValueError('Container Number must be exactly 11 characters long.')
            if not record.container_number[:4].isalpha() or not record.container_number[:4].isupper():
                raise ValueError('The first 4 characters must be capital letters.')
            if not record.container_number[4:].isdigit():
                raise ValueError('The last 7 characters must be digits.')
            if record.container_number[3] != 'U':
                raise ValueError('The last character must be "U".')

    is_option = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('special_equ', 'Special Equ')
    ],
    string='Is:',
    default='dry'
    )
    tare_weight = fields.Float(string='Tare Weight (KG)')
    max_load = fields.Float(string='Max Load (KG)'
                            )
    status = fields.Boolean(string='Status', default=True)
