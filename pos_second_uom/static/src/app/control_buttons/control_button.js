/** @odoo-module **/

import { AddQuantityDialog } from "./dialog_box/add_quantity_dialog";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
        this.dialog = useService("dialog");
        this.pos = this.env.services.pos;
    },

    get secondUomName() {
        const line = this.pos.get_order().get_selected_orderline();
        return line?.get_product()?.pos_second_uom_id?.name;
    },

    get shouldShowAddQtyButton() {
        const order = this.pos.get_order();
        const line = order?.get_selected_orderline();
        return !!line?.get_product()?.pos_second_uom_id;
    },

    onAddQuantity() {
        const order = this.pos.get_order();
        const line = order.get_selected_orderline();

        if (!line || !line.get_product()?.pos_second_uom_id) {
            return;
        }

        this.dialog.add(AddQuantityDialog, {
            product: line.get_product(),
            orderline: line,
            secondUomName: this.secondUomName,
        });
    },
});
