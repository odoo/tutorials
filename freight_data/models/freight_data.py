from odoo import api, fields, models


class PortCity(models.Model):
    _name = 'freight.data'
    _description = 'Freight Data Model'

    code = fields.Char(string='Code')
    name = fields.Char(string='Name')
    country_id = fields.Many2one('res.country', string='Country')
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True, readonly=True)
    transport_modes = fields.Selection([
        ('air', 'Air'),
        ('sea', 'Sea'),
        ('inland', 'Inland')
    ], string='Is:')
    status = fields.Boolean(string='Status', default=True)

    @api.depends('name', 'country_id')
    def _compute_display_name(self):
        for record in self:
            if self.name and self.country_id:
                record.display_name = f"{record.name} - {record.country_id.name}"
