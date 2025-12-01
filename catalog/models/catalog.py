from odoo import api, fields, models


class Catalog(models.Model):
    _name = 'catalog'
    _description = 'Model to make catalogs for products based on product categories'

    name = fields.Char(required=True)
    date = fields.Date(string="Created Date", compute="_compute_create_date", store=True)
    line_ids = fields.One2many("catalog.line", "catalog_id", string="Lines")
    field_ids = fields.One2many("catalog.field", "catalog_id", string="Fields")

    @api.depends("create_date")
    def _compute_create_date(self):
        for record in self:
            record.date = record.create_date.date() if record.create_date else False

    def open_catalog_kanban_view(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Catalog Product Kanban',
            'res_model': 'product.product',
            'view_mode': 'kanban',
            'view_id': self.env.ref('catalog.view_catalog_product_kanban').id,
            'search_view_id': self.env.ref('catalog.product_kanban_search_catalog').id,
            'target': 'current',
        }


class CatalogLine(models.Model):
    _name = "catalog.line"
    _description = "Catalog Line"

    catalog_id = fields.Many2one("catalog", string="Catalog", readonly=True)
    category_id = fields.Many2one("product.category", string="Category ID")
    category_name = fields.Char(string="Category", compute="_compute_category", store=True)
    color_1 = fields.Char(string="Color 1")
    color_2 = fields.Char(string="Color 2")
    removed_products = fields.Many2many(
        'product.product',
        'catalog_line_removed_products_rel',
        'catalog_line_id', 'product_id',
        string="Removed Products"
    )

    @api.depends("category_id")
    def _compute_category(self):
        for record in self:
            record.category_name = record.category_id.name if record.category_id else ""


class CatalogField(models.Model):
    _name = "catalog.field"
    _description = "Catalog Field"

    catalog_id = fields.Many2one("catalog", string="Catalog", readonly=True)
    sequence = fields.Integer(default=1)
    field_name = fields.Selection([
        ('name', "Name"),
        ('lst_price', "Price"),
        ('image_1920', "Image"),
        ('qty_available', "Quantity On Hand"),
    ], string='Field Name')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            existing_field = self.search([
                ('catalog_id', '=', vals.get('catalog_id')),
                ('field_name', '=', vals.get('field_name'))
            ], limit=1)

        if existing_field:
            return

        return super().create(vals_list)
