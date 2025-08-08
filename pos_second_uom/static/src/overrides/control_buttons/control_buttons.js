/** @odoo-module **/

import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { SecondUomDialog } from "./second_uom_dialog/second_uom_dialog";

patch(ControlButtons.prototype,{
    get secondUomName(){        
        return this.currentOrder.get_selected_orderline().product_id.pos_second_uom_id?.name;
    },
    setSecondUom(){
        const orderLine = this.currentOrder?.get_selected_orderline();
        if (!orderLine || !this.secondUomName) {
            this.notification.add("No Second UoM available for this product.", { type: "warning" });
            return;
        }
        const product = this.currentOrder.get_selected_orderline().get_product();         
        this.dialog.add(SecondUomDialog,{
            product,
            secondUomName: this.secondUomName
        })
    }
})
