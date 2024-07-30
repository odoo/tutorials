from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Container(models.Model):
    _name = 'containers'
    _description = 'Container'
    name = fields.Char(string="Name")
    container_number = fields.Char(string='Container Number', required=True)
    container_type_id = fields.Many2one('container.type', string='Container Type', required=True, domain=[('status', '=', True)])
    container_type = fields.Selection(
        selection=[
            ('dry', 'Dry'),
            ('reefer', 'Reefer'),
            ('special', 'Special Equ.')
        ], string='Is', required=True)
    container_owner_id = fields.Many2one('res.partner', string='Container Owner', required=True)
    tare_weight = fields.Float(string='Tare Weight (KG)', required=True)
    max_load = fields.Float(string='Max Load (KG)', required=True)
    status = fields.Boolean(string='Status', default=True)

    @api.constrains('container_number')
    def _check_container_number(self):
        for record in self:
            if not re.match(r'^[A-Z]{3}U\d{7}$', record.container_number):
                raise ValidationError("Container Number must be 4 capital letters ending by 'U' and 7 numbers. Example: TEMU1152206")
