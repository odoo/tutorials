from odoo import api, fields, models
from odoo.exceptions import ValidationError
import re


class FreightContainers(models.Model):
    _name = "freight.containers"
    _description = "Freight Containers Model"

    container_number = fields.Char('Container Number', required=True)
    container_type_id = fields.Many2one(
        'freight.container.type',
        string='Container Type',
        required=True,
        domain=[('status', '=', '')]
    )
    is_options = fields.Selection([
            ('dry', 'Dry'),
            ('reefer', 'Reefer'),
            ('special_equ', 'Special Equipment')
        ], string='Is', required=True
    )
    container_owner_id = fields.Many2one(
        'res.partner',
        string='Container Owner',
        required=True
    )
    tare_weight = fields.Float(string='Tare Weight (KG)', required=True)
    max_load = fields.Float(string='Max Load (KG)', required=True)
    status = fields.Boolean(string="Status", default=True)

    @api.constrains('container_number')
    def _check_container_number(self):
        pattern = re.compile(r'^[A-Z]{3}U\d{7}$')
        for record in self:
            if not pattern.match(record.container_number):
                raise ValidationError("Container Number must be in the format of 4 capital letters, followed by 'U' and 7 digits.")
