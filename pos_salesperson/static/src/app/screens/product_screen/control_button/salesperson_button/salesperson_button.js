import {Component} from "@odoo/owl"
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";
import { useState } from "@odoo/owl";

export class SalesPersonButton extends Component{
    static template = "pos_salesperson.SelectSalespersonButton" 
    
    setup(){
        this.pos = usePos();
        this.dialog = useService("dialog");
        this.salesperson = useState({ name: "Salesperson" }); 
    }

    async onClick() {

        const employees = this.pos.models['hr.employee'].getAll()
        const currentOrder = this.pos.get_order()
        const selectionList = employees.map((employee) => ({
            id: employee.id,
            item: employee,
            label: employee.name,
            isSelected: false,
        }));
        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: "Salesperson",
            list: selectionList
        })
        if (payload) {
            console.log("Payload")
            this.salesperson.name = payload.name;
            currentOrder.setSalesPerson(payload.id)
        }
    }
}
