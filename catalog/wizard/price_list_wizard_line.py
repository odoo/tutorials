# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PriceListWizardLine(models.TransientModel):
    _name = 'price.list.wizard.line'
    _description = "Price List Wizard Line"

    list_id = fields.Many2one(comodel_name='price.list.wizard')
    so_date = fields.Date(string="Date")
    price = fields.Float(string="Price")
