import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";

patch(PosStore.prototype, {
    async SelectSalesperson() {
        this.dialog = this.env.services.dialog;
        const currentOrder = this.pos.get_order();

        if (!currentOrder) {
            console.warn("No active order found.");
            return;
        }
        const salesperson_list = this.pos.models['hr.employee'].map((person) => ({
            id: person.id,
            item: person,
            label: person.name,
        }));

        const currentSalesperson = await makeAwaitable(this.dialog, SelectionPopup, {
            title: "Select A SalesPerson",
            list: salesperson_list,
        });

        if (currentSalesperson) {
            this.props.salesperson = currentSalesperson;
            currentOrder.salesperson_id = currentSalesperson;
            this.render();
        }
    },
});
