import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";
import { useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks"; 
import { AlertDialog } from "@web/core/confirmation_dialog/confirmation_dialog";


patch(ControlButtons.prototype, {
    setup() {
        super.setup()
        this.dialogService = useService("dialog");
        this.salesperson = useState({ name: "Salesperson" }); 
    },

    async selectSalesperson() {
        const currentOrder = this.pos.get_order();
        const employees = this.pos.models['hr.employee'] || [];  

        if (!employees.length) {
            this.dialogService.add(AlertDialog, {
                body: "No employees found!",
                title: "Missing Data"
            })
            return;
        }

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
            this.salesperson.name = payload.name;
            currentOrder.setSalesPerson(payload.id)
        }
    }
});


