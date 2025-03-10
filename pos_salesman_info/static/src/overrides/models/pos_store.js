import { PosStore } from "@point_of_sale/app/store/pos_store";
import { makeActionAwaitable } from "@point_of_sale/app/store/make_awaitable_dialog";
import { patch } from "@web/core/utils/patch";

patch(PosStore.prototype, {
    async editSalesperson(sales_person) {
        const record = await makeActionAwaitable(
            this.action,
            "pos_salesman_info.open_view_employee",
            {
                props: { resId: sales_person?.id },
            }
        );
        const newSalesPerson = await this.data.read("hr.employee", record.config.resIds);
        return newSalesPerson[0];
    }
})
