import { Component, useState } from "@odoo/owl";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import {makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";

export class SelectSalespersonButton extends Component{
    static template = "pos_salesperson.SelectSalespersonButton";
    static props = ["salesperson?"];

    setup(){
        this.pos = usePos();
        this.ui - useState(useService("ui"));
        this.dialog = useService("dialog");
        this.orm = useService("orm");
    }

    async onClick(){
        const currentOrder = this.pos.get_order();
        console.log(currentOrder);

        if (!currentOrder) {
            return;
        }
        const employees = await this.orm.searchRead("hr.employee", [], ["id", "name"]);

        console.log("employees", employees);

        if (!employees || employees.length === 0) {
            this.dialog.add(AlertDialog, {
                title: "No Salespersons Found",
                body: "No salesperson records are available.",
            });
            return;
        }
        console.log("Opening SelectionPopup...");
        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: "Select Salesperson",
            list: employees.map(emp => ({ id: emp.id, label: emp.name, item: emp, isSelected: false })),
        });

        console.log("Salesperson ID:", currentOrder.salesperson_id);
        console.log("Salesperson Name:", currentOrder.salesperson_name);

        console.log("Payload:", payload);

        if (payload) {
            currentOrder.set_salesperson(payload);
        } else {
            console.warn("No Salesperson selected");
        }

        console.log("Updated Salesperson ID:", currentOrder.salesperson_id);
        console.log("Updated Salesperson Name:", currentOrder.salesperson_name);

    }

}
