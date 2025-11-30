# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


CATEGORY_SELECTION = [
    ('readonly', 'Readonly'),
    ('editable', 'Editable'),
    ('no', 'None'),
]


class ApprovalCategory(models.Model):
    _inherit = 'approval.category'

    approval_type = fields.Selection(selection_add=[('sales', 'Create Sale\'s')])
    has_sale_product = fields.Selection(CATEGORY_SELECTION, string="Has Sale Product", default="no")
    has_sale_quantity = fields.Selection(CATEGORY_SELECTION, string="Has Sale Quantity", default="no")
    has_unit_price = fields.Selection(CATEGORY_SELECTION, string="Has Unit Price", default="no")
    has_cost_price = fields.Selection(CATEGORY_SELECTION, string="Has Cost Price", default="no")
    has_margin = fields.Selection(CATEGORY_SELECTION, string="Has Margin", default="no")
    has_margin_custom = fields.Selection(CATEGORY_SELECTION, string="Has Margin Custom", default="no")
    has_final_price = fields.Selection(CATEGORY_SELECTION, string="Has Final Price", default="no")
