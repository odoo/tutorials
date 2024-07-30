from odoo import models, fields, api

class Ports(models.Model):
    _name = 'ports'
    _description = 'Port'

    name = fields.Char(string='Port Name')
    code = fields.Char(string="Code")
    country = fields.Many2one("res.country", string="Country", required=True)
    active = fields.Boolean(string="Active", default=True)
    display_name = fields.Char(string="Display Name", compute="_compute_display_name", readonly=True)
    freight_is_port_id = fields.Many2many("freight.is.port", string="Is option")
    full_name = fields.Char(string="Full Name")

    @api.depends('name', 'country')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.country:
                record.display_name = f"{record.name} - {record.country.name}"
            else:
                record.display_name = ''
