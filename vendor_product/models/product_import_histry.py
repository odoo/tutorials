from odoo import fields, models


class ProductImportHistry(models.Model):
    _name = 'product.import.histry'

    import_reference = fields.Char("Import Reference")
    date_of_import = fields.Date("Date Of Import")
    file_name = fields.Char("File Name")
    old_price = fields.Integer("Old Price")
    new_price = fields.Integer("New Price")
    product_id = fields.Many2one('product.template')
