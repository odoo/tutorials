from odoo import api, fields, models


class FreightData(models.Model):
    _name = 'freight.data'
    _description = 'Freight Data Model'

    code = fields.Char(string='Code', required=True)
    name = fields.Char(string='Name', required=True)
    country_id = fields.Many2one(comodel_name='res.country', string='Country: ', required=True, domain="[('id', '!=', False)]", options={'no_create': True, 'no_open': True})
    display_name = fields.Char(string='Display Name', compute='_compute_display_name', store=True, readonly=True)
    is_selection_ids = fields.Many2many(comodel_name='freight.selection', string='Is')
    status = fields.Boolean(string='Status', default=True)

    @api.depends('name', 'country_id')
    def _compute_display_name(self):
        for freight_data in self:
            freight_data.display_name = (freight_data.name and freight_data.country_id) and f"{freight_data.name} - {freight_data.country_id.name}" or ""
