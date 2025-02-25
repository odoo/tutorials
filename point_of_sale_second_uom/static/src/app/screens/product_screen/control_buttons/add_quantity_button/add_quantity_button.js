import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { AddQuantityDialog } from "./dialog/add_quantity_dialog";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useState } from "@odoo/owl";

patch(ControlButtons.prototype, {
    setup() {
        this.pos = usePos();
        this.ui = useState(useService("ui"));
    },
    get currentOrder() {
        return this.pos.get_order();
    },
    get product(){
        return this.pos.selectedOrder.get_selected_orderline().product_id
    },
    onAddQuantity() {
        const second_uom = this.product.second_uom_id.name
        const primary_factor = this.product.uom_id.factor
        const secondary_factor = this.product.second_uom_id.factor
        this.env.services.dialog.add(AddQuantityDialog, {
            second_uom,
            confirm: (quantity) => {
                this.pos.selectedOrder.get_selected_orderline().set_quantity(quantity*(primary_factor/secondary_factor))
            },
            close: () => {
                console.log("Dialog discarded");
            },
        });
    },
});
