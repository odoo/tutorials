from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dosage_per_ton = fields.Float(
        string="Dosage (Kg/Ton)",
        help="How many Kg of this product are needed per 1 ton.",
        digits=(16, 4),
    )

    extra_categ_ids = fields.Many2many(
        comodel_name='product.category',
        relation='product_template_extra_category_rel',
        column1="product_tmpl_id",
        column2="categ_id",
        string="Extra Categories",
        help="Additional categories for this product"
    )

    all_categ_ids = fields.Many2many(
        comodel_name="product.category",
        compute="_compute_all_categ_ids",
        store=True,
        string="All Categories",
        help="Main category + extra categories. Useful for searching/grouping.",
    )

    @api.depends("categ_id", "extra_categ_ids")
    def _compute_all_categ_ids(self):
        for product in self:
            cats = product.extra_categ_ids
            if product.categ_id:
                cats |= product.categ_id
            product.all_categ_ids = cats

    @api.constrains("dosage_per_ton")
    def _check_dosage_non_negative(self):
        for p in self:
            if p.dosage_per_ton < 0:
                raise ValidationError(_("Dosage cannot be negative."))