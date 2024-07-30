from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class FreightContainer(models.Model):
    _name = 'freight.container'
    _description = 'Container'

    name = fields.Char(string='Display Name', store=True)
    container_number = fields.Char(string='Container Number', required=True)
    container_type_id = fields.Many2one('container.type', string='Container Type', required=True)
    is_type = fields.Selection([
        ('dry', 'Dry'),
        ('reefer', 'Reefer'),
        ('special_equipment', 'Special Equipment')
    ], string='Is', required=True)
    container_owner_id = fields.Many2one('res.partner', string='Container Owner', required=True)
    tare_weight = fields.Float(string='Tare Weight (KG)', required=True)
    max_load = fields.Float(string='Max Load (KG)', required=True)
    status = fields.Boolean(string='Status', default=True)

    @api.constrains('container_number')
    def _check_container_number(self):
        pattern = re.compile(r'^[A-Z]{4}U\d{7}$')
        for record in self:
            if not pattern.match(record.container_number):
                raise ValidationError("Container Number must be 4 capital letters followed by 'U' and 7 numbers (e.g., TEMU1152206).")
