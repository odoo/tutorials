from odoo import _, api, Command, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    has_bom = fields.Boolean(string=_("Has Bills of Materials"), compute='_compute_has_bom', store=True)

    @api.model
    def _get_route(self, xml_id, route_name):
        """Generic method to get a route by xml_id or name"""
        route = self.env.ref(xml_id, raise_if_not_found=False)
        if not route:
            route = self.env['stock.route'].search([('name', '=', route_name)], limit=1)
        return route

    @api.depends('bom_ids')
    def _compute_has_bom(self):
        for product in self:
            product.has_bom = bool(product.bom_ids)

    @api.onchange('purchase_ok')
    def _onchange_purchase_ok(self):
        """Automatically handle buy route when purchase option changes"""
        buy_route = self._get_route('purchase_stock.route_warehouse0_buy', 'Buy')
        if not buy_route:
            return

        if self.purchase_ok:
            # Only add if not already in the routes
            if buy_route.id not in self.route_ids.ids:
                self.route_ids = [Command.link(buy_route.id)]
        else:
            # Remove from routes
            if buy_route.id in self.route_ids.ids:
                self.route_ids = [Command.unlink(buy_route.id)]

    @api.model
    def create(self, vals):
        """Override create to automatically manage routes"""
        product = super().create(vals)
        product._update_routes_based_on_config()
        return product

    def write(self, vals):
        """Override write to automatically manage routes"""
        result = super().write(vals)
        if any(field in vals for field in ['purchase_ok', 'route_ids']):
            self._update_routes_based_on_config()
        return result

    def _is_subcontract_component(self):
        """check if product is used as a component in any subcontracting BOM"""
        self.ensure_one()
        boms = self.env['mrp.bom'].search([('type', '=', _('subcontract'))])
        for bom in boms:
            if bom.bom_line_ids.filtered(lambda bom_line: bom_line.product_id.product_tmpl_id.id == self.id):
                return True
        return False

    def _handle_dropship_routes(self):
        """Handle dropship routes based on product context

        This method manages both regular dropship and dropship subcontractor routes:
        - If product is a component in a subcontracting BOM and dropship is enabled,
          apply the dropship subcontractor route
        - Otherwise, apply the regular dropship route if enabled
        """
        self.ensure_one()

        dropship_route = self._get_route('stock_dropshipping.route_drop_shipping', 'Dropship')
        dropship_subcontractor_route = self._get_route('mrp_subcontracting_dropshipping.route_subcontracting_dropshipping', 'Dropship Subcontractor on Order')
        if not dropship_route or not dropship_subcontractor_route:
            return []

        route_commands = []
        is_subcontract_component = self._is_subcontract_component()

        # Check if regular dropship is enabled
        dropship_enabled = dropship_route.id in self.route_ids.ids

        # Handle dropship subcontractor route for components in subcontracting BOMs
        if is_subcontract_component and dropship_enabled:
            # Add dropship subcontractor route if not already present
            if dropship_subcontractor_route.id not in self.route_ids.ids:
                route_commands.append(Command.link(dropship_subcontractor_route.id))
        elif dropship_subcontractor_route.id in self.route_ids.ids:
            # Remove dropship subcontractor route if not needed
            route_commands.append(Command.unlink(dropship_subcontractor_route.id))

        return route_commands

    def _update_routes_based_on_config(self):
        """Update routes based on product configuration

        This method ensures that routes are correctly assigned based on:
        - Purchase configuration (Buy route)
        - Manufacturing configuration (Manufacture route)
        - Subcontracting usage (Subcontract route)

        It will add or remove routes as needed without user intervention.
        """
        buy_route = self._get_route('purchase_stock.route_warehouse0_buy', 'Buy')
        manufacture_route = self._get_route('mrp.route_warehouse0_manufacture', 'Manufacture')
        subcontract_route = self._get_route('mrp_subcontracting.route_resupply_subcontractor_mto', 'Resupply Subcontractor on Order')

        for product in self:
            route_commands = []
            
            # Handle Buy route
            if product.purchase_ok and buy_route and buy_route.id not in product.route_ids.ids:
                route_commands.append(Command.link(buy_route.id))
            elif not product.purchase_ok and buy_route and buy_route.id in product.route_ids.ids:
                route_commands.append(Command.unlink(buy_route.id))
            
            # Handle Manufacture route
            if product.has_bom and manufacture_route and manufacture_route.id not in product.route_ids.ids:
                route_commands.append(Command.link(manufacture_route.id))
            elif not product.has_bom and manufacture_route and manufacture_route.id in product.route_ids.ids:
                route_commands.append(Command.unlink(manufacture_route.id))
            
            # Handle Subcontract route (components used in subcontracting BoMs)  
            is_subcontract_component = False
            if subcontract_route:
                is_subcontract_component = self._is_subcontract_component()
            
            if is_subcontract_component and subcontract_route.id not in product.route_ids.ids:
                route_commands.append(Command.link(subcontract_route.id))
            elif not is_subcontract_component and subcontract_route.id in product.route_ids.ids:
                route_commands.append(Command.unlink(subcontract_route.id))
            
            # Handle Dropship routes
            dropship_commands = product._handle_dropship_routes()
            if dropship_commands:
                route_commands.extend(dropship_commands)

            if route_commands:
                product.write({'route_ids': route_commands})
