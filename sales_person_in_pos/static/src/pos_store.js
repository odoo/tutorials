import { patch } from "@web/core/utils/patch";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { makeAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { SelectionPopup } from "@point_of_sale/app/utils/input_popups/selection_popup";

patch(PosStore.prototype, {

    async selectSalesPerson() {
        const currentOrder = this.get_order();
        const salesperson_list = this.models['hr.employee'].map((sp) => {
            return {
                id: sp.id,
                item: sp,
                label: sp.name,
                isSelected: currentOrder.getSalesperson()?.id === sp.id
            }
        });

        const selected_salesperson = await makeAwaitable(
            this.dialog,
            SelectionPopup,
            {
                title: "Select Salesperson",
                list: salesperson_list,
            }
        );

        if (selected_salesperson) {
            const existing_salesperson = currentOrder.getSalesperson();
            if (!(existing_salesperson?.id === selected_salesperson?.id)) {
                currentOrder.setSalesperson(selected_salesperson);
            } else {
                currentOrder.setSalesperson(false)
            }
        }
    }
});
