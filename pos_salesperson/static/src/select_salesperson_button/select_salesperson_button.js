import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";

export class SelectSalespersonButton extends Component {
    static template = "pos_salesperson.SelectSalespersonButton";

    setup() {
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.orm = useService("orm");
        this.salesperson = useState({ name: "Salesperson" });
    }

    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        const employees = this.pos.models['hr.employee'] || [];

        if(!employees.length){
            this.dialog.add(AlertDialog, {
                title: "No Salespersons Found",
                body: "No salesperson records are available.",
            });
            return;
        }

        const selectionList = employees.map((emp) => ({
            id : emp.id,
            item : emp,
            label : emp.name,
            isSelected : false,
        }));

        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: "Select Salesperson",
            list: selectionList
        })

        if(payload){
            this.salesperson.name = payload.name;
            currentOrder.set_salesperson(payload.id)
        }
    }

}
