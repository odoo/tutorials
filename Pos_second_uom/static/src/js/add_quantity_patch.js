/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SecondaryUomDialog } from "./add_quantity_button";


patch(ControlButtons.prototype, {
    async openSecondaryUomDialog() {
        const order = this.pos.get_order();
        const orderline = order.get_selected_orderline();

        if (!orderline.product_id.uom_id.category_id.uom_ids[1]) {
            this.env.services.notification.add("Select a product with a secondary UoM first.", {
                type: "warning",
            });
            return;
        }

        this.dialog.add(SecondaryUomDialog, {
            orderline,
        });
    },
});
