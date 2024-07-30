from odoo import api, fields, models


class FreightPortsCities(models.Model):
    _name = "freight.ports.cities"
    _description = "Freight Ports and Cities Model"
    _inherits = {'freight.data': 'inherit_data'}

    inherit_data = fields.Many2one(
        comodel_name='freight.data',
        ondelete='cascade'
    )
    country = fields.Many2one(
        comodel_name="res.country",
        string="Country",
        required=True,
        options="{'no_open': True, 'no_create': True}",
    )
    is_options = fields.Many2many(
        comodel_name="freight.is.options",
        string="Is:",
        required=True
    )
    display_name = fields.Char(string="Display Name", compute='_compute_display_name', store=True, readonly=True)

    @api.depends('name', 'country')
    def _compute_display_name(self):
        for record in self:
            if record.name and record.country:
                record.display_name = f"{record.name} - {record.country.name}"
