from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class ProductKitLine(models.Model):
    _name = 'product.kit.line'
    _description = 'Product Kit Line'
    _rec_name = 'product_id'

    product_tmpl_id = fields.Many2one(
        'product.template',
        string="Kit Product",
        required=True,
        ondelete='cascade',
    )
    product_id = fields.Many2one(
        'product.product',
        string="Component Product",
        required=True,
    )
    quantity = fields.Float(
        string="Quantity",
        required=True,
        default=1.0,
    )

    @api.constrains('product_id')
    def _check_product_id(self):
        """Validate that the component product is not the same as the kit product itself."""
        for line in self:
            if line.product_id and line.product_id.product_tmpl_id == line.product_tmpl_id:
                raise ValidationError(
                    _("A product cannot be a component of itself.")
                )

    def write(self, vals):
        """Prevent modification of restricted fields after creation."""
        restricted_fields = {'product_id', 'quantity', 'product_tmpl_id'}
        modified = restricted_fields & set(vals.keys())
        if modified:
            field_names = dict(self.fields_get(modified)).keys()
            raise UserError(
                _("Kit line fields (%s) cannot be modified after creation. "
                  "Delete and recreate the line instead.")
                % ", ".join(field_names)
            )
        return super(ProductKitLine, self).write(vals)
