import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { AddQuantityDialog } from "./dialog/add_quantity_dialog";


patch(ControlButtons.prototype, {
    onAddQuantity() {
        const product = this.pos.selectedOrder.get_selected_orderline()?.product_id
        const second_uom = product.second_uom_id
        const quantity = this.pos.selectedOrder.get_selected_orderline().qty*(second_uom.factor/product.uom_id.factor)
        this.env.services.dialog.add(AddQuantityDialog, {
            second_uom: second_uom.name, quantity,
            confirm: (quantity) => {
                this.pos.selectedOrder.get_selected_orderline().set_quantity(quantity*(product.uom_id.factor/second_uom.factor))
            },
        });
    },
});
