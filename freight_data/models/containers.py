from odoo import api, models, fields
from odoo.exceptions import ValidationError
CONTAINER_TYPE = [
    ('dry', 'Dry'),
    ('reefer', 'Reefer'),
    ('special_equipment', 'Special Equipment')
]


class Containers(models.Model):
    _name = "containers"
    _description = "Containers"

    container_number = fields.Char(string='Container No.', required=True)
    container_type_id = fields.Many2one('container.type', string='Container Type', required=True, domain="[('status', '=', 'True')]")
    is_type = fields.Selection(string='Is', selection=CONTAINER_TYPE, required=True)
    container_owner_id = fields.Many2one('res.partner', string='Container Owner', required=True)
    tare_weight = fields.Float(string='Tare Weight (KG)', required=True)
    max_load = fields.Float(string='Max Load (KG)', required=True)
    status = fields.Boolean(string='Status', default=True)

    @api.constrains('container_number')
    def _check_container_number(self):
        for record in self:
            container_number = record.container_number
            valid_length = len(container_number) == 11
            valid_first_three = container_number[:3].isalpha() and container_number[:3].isupper() if valid_length else False
            valid_fourth_char = container_number[3] == 'U' if valid_length else False
            valid_digits = len(container_number) >= 10 and container_number[4:10].isdigit() and container_number[10].isdigit() if valid_length else False

            if not all([valid_length, valid_first_three, valid_fourth_char, valid_digits]):
                raise ValidationError(
                    "Container Number must be exactly 11 characters long, with the first 3 characters as uppercase letters, "
                    "the 4th character as 'U', followed by 6 digits and ending with a digit. Example: TEMU1152206."
                )
