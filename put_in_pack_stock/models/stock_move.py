from odoo import api, models, fields
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    # Boolean field to control whether the 'Put in Pack' button is visible 
    # based on the related picking type's configuration.
    put_in_pack_toggle = fields.Boolean(
        string="Put In Pack",
        related="picking_type_id.put_in_pack_toggle"
    )
    # Field to define the number of packages to create.
    package_qty = fields.Integer(
        string="Package Qty:",
        help="Number of packages to create for the product.",
        default=1
    )
    # Selection field to specify the type of package used (e.g., Box or Carton).
    package_type = fields.Selection(
        selection=[
            ('box', "Box"),
            ('carton', "Carton")
        ],
        string="Package Type",
        help="Defines the type of package used for the product."
    )
    # Field to define the maximum quantity of the product that fits into one package.
    package_size = fields.Integer(
        string="Package Size",
        help="Number of product units contained in each package.",
        default=0
    )
    def make_package(self):
        """Creates a new stock package with a name based on the product."""
        package = self.env['stock.quant.package'].create({
            'name': f"{self.product_id.name} Package"
        })
        return package
    def make_move_line(self, package, qty_done, lot_id=False, lot_name=False):
        """
        Creates a stock move line linked to the given package.
        
        :param package: The package where the product will be moved.
        :param qty_done: The quantity of the product in the package.
        :param lot_id: (Optional) Lot ID if tracking by lot.
        :param lot_name: (Optional) Lot name if tracking by lot.
        """
        self.env['stock.move.line'].create({
            'move_id': self.id,
            'result_package_id': package.id,
            'qty_done': qty_done,  # Uses the total quantity of the product
            'product_id': self.product_id.id,
            'product_uom_id': self.product_id.uom_id.id,
            'lot_id': lot_id,
            'lot_name': lot_name
        })
    def action_custom_put_in_pack(self):
        """
        Custom action to package the entire quantity of the product in one package.
        - Ensures that there is available quantity to package.
        - Removes existing move lines before packaging.
        - Creates a new package and assigns the move line to it.
        """
        self.ensure_one()
        if self.product_uom_qty <= 0:
            raise UserError("No quantity available to package.")
        # Remove existing move lines before creating a new packaged move line
        self.move_line_ids.unlink()
        # Create a new package and assign the entire quantity
        package = self.make_package()
        self.make_move_line(package=package, qty_done=self.product_uom_qty)
    def action_generate_package(self):
        """
        Generates multiple packages based on package size and tracking type.
        - If tracking is none, the product is split into multiple packages.
        - If tracking is by lot, packages are created per lot.
        """
        self.ensure_one()
        # Case: No tracking (all quantities can be freely split into packages)
        if self.has_tracking == 'none':
            self.move_line_ids.unlink()
            demand = self.product_uom_qty
            correct_uom = self.product_id.uom_id.id
            if not correct_uom:
                raise ValueError(f"Product {self.product_id.name} does not have a valid UoM set!")
            # Create the required number of packages based on demand and package size
            for _ in range(self.package_qty):
                if demand <= 0:
                    break
                package = self.make_package()
                qty_to_pack = min(demand, self.package_size)
                self.make_move_line(package=package, qty_done=qty_to_pack)
                demand -= qty_to_pack
        # Case: Tracking by lot (each lot must be packaged separately)
        elif self.has_tracking == 'lot':
            correct_uom = self.product_id.uom_id.id
            temp_store_package = []
            for line in self.move_line_ids:
                lot_quantity = line.quantity
                lot_id = self.id
                # Split each lot quantity into separate packages
                while lot_quantity:
                    package = self.make_package()
                    qty_to_pack = min(lot_quantity, self.package_size)
                    # Store package details before creating move lines
                    temp_store_package.append({
                        'lot_id': line.lot_id.id,
                        'lot_name': line.lot_name,
                        'result_package_id': package,
                        'qty_done': qty_to_pack
                    })
                    lot_quantity -= qty_to_pack
            # Remove old move lines before creating new ones
            self.move_line_ids.unlink()
            # Assign products to the newly created packages
            for package_data in temp_store_package:
                self.make_move_line(
                    package=package_data['result_package_id'],
                    qty_done=package_data['qty_done'],
                    lot_id=package_data['lot_id'],
                    lot_name=package_data['lot_name']
                )
