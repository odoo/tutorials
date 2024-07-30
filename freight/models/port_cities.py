from odoo import api, models, fields


class PortCities(models.Model):
    _name = "port.cities"
    _description = "Port and Cities"

    code = fields.Char(string="Code")
    name = fields.Char(string="Name")
    country_id = fields.Many2one(
        'res.country',
        string='Country',
        required=True,
        options={'no_create': True, 'no_create_edit': True},
        domain="[('id', '!=', False)]"
    )
    display_name = fields.Char(string='Display Name', readonly=True, compute='_compute_display_name')
    status = fields.Boolean(string='Status', default=True)
    is_air = fields.Boolean(string='Is Air')
    is_sea = fields.Boolean(string='Is Sea')
    is_inland = fields.Boolean(string='Is Inland')

    @api.depends('name', 'country_id')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.country_id:
                record.display_name = f"{record.name} - {record.country_id.name}"
            else:
                record.display_name = ''
