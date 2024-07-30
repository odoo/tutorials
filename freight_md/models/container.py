from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Container(models.Model):
    _name = 'container'
    _description = 'Container'

    container_number = fields.Char('Display name', required=True, copy=False)
    container_type_id = fields.Many2one('container.type', string='Container Type', required=True, domain=[('status', '=', True)])
    is_type = fields.Selection([('dry', 'Dry'), ('reefer', 'Reefer'), ('special', 'Special Equ.')], string='Type', required=True)
    container_owner_id = fields.Many2one('res.partner', string='Owner', required=True)
    tare_weight = fields.Float('Tare Weight (KG)', required=True)
    max_load = fields.Float('Max Load (KG)', required=True)
    status = fields.Boolean('Status', default=True)

    @api.constrains('container_number')
    def _check_container_number(self):
        for record in self:
            container_number = record.container_number
            if len(container_number) != 11:
                raise ValidationError("Container Number must be exactly 11 characters long.")
            if not (container_number[:4].isalpha() and container_number[:4].isupper()):
                raise ValidationError("Container Number must start with 4 uppercase letters.")
            if not (container_number[4:10].isdigit() and container_number[3] == 'U'):
                raise ValidationError("Container Number must end with 'U' followed by 7 digits.")
