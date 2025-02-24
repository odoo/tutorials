import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { AddQuantityDialog } from "./add_quantity_dialog/add_quantity_dialog";

patch(ControlButtons.prototype, { 
    setup(){
        super.setup();
        this.pos = usePos();
        this.ui = useState(useService("ui"));
        this.dialog = useService("dialog");
    },

    get secondUomName(){
        return this.currentOrder.get_selected_orderline().product_id.second_uom_id?.name;
    },

    onAddQuantity(){
        const product = this.currentOrder.get_selected_orderline().get_product();
        this.dialog.add(AddQuantityDialog, {
            product,
            secondUomName: this.secondUomName,
        });
    },
});
