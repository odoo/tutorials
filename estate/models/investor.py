from odoo import fields, models


class InvestorProfile(models.Model):
    _name = 'investor'
    _description = "inverstor model"

    inv = fields.Many2one(
        'res.partner', string="investor", copy=False, ondelete='cascade'
    )
