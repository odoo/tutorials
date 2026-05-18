from odoo import fields, models


class PharmacyCategory(models.Model):
    _name = "pharmacy.category"
    _description = "Medicine Category"
    _order = "name"

    name = fields.Char(string="Category Name", required=True, translate=True)
    code = fields.Char(string="Category Code", help="Short code, e.g., ANTIBIOTIC")
    description = fields.Text(string="Description")
    parent_id = fields.Many2one('pharmacy.category', string="Parent Category", ondelete='restrict')
    child_ids = fields.One2many('pharmacy.category', 'parent_id', string="Child Categories")
