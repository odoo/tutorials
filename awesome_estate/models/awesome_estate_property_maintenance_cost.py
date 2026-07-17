from odoo import fields, models


class AwesomeEstatePropertyMaintenanceCost(models.Model):
    _name = 'awesome.estate.property.maintenance.cost'
    _description = 'Maintenance Cost Line'
    _rec_name = 'name'
    _order = 'date desc, id desc'

    # -----------------------------------------------------------------------
    # Fields
    # -----------------------------------------------------------------------
    currency_id = fields.Many2one(
        'res.currency',
        related='maintenance_id.currency_id',
        store=True,
    )
    maintenance_id = fields.Many2one(
        'awesome.estate.property.maintenance',
        string="Maintenance Request",
        required=True,
        ondelete='cascade',
    )
    name = fields.Char(string="Description", required=True)
    amount = fields.Monetary(
        string="Amount",
        currency_field='currency_id',
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.context_today,
    )
