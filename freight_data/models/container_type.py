from odoo import models, fields

CONTAINER_TYPE = [
    ('dry', 'Dry'),
    ('reefer', 'Reefer'),
    ('special_equipment', 'Special Equipment')
]


class ContainerType(models.Model):
    _name = "container.type"
    _description = "Container Type"

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    is_type = fields.Selection(string='Is', selection=CONTAINER_TYPE, required=True)
    size = fields.Float(string='Size')
    volume = fields.Float(string='Volume')
    status = fields.Boolean(string='Status', default=True)
