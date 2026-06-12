from odoo import models, fields


class Expense(models.Model):
    _name = 'tutorials.expense'
    _description = 'Expense'

    CATEGORY_SELECTION = [
        ('shopping', 'Shopping'),
        ('food', 'Food'),
        ('travel', 'Travel'),
        ('other', 'Other'),
    ]

    category = fields.Selection(CATEGORY_SELECTION, required=True, default='other')
    price = fields.Float(required=True)
    description = fields.Text()
    date = fields.Datetime(default=fields.Datetime.now)
