import { patch } from "@web/core/utils/patch";
import { makeActionAwaitable , makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { EmployeeList } from "./employee_list/employee_list";

patch(PosStore.prototype, {
    async setup() {
        await super.setup(...arguments);
    },

    async editEmployee(employee) {
        const record = await makeActionAwaitable(
            this.action,
            "pos_orderline_employee.hr_employee_action_edit_pos",
            {
                props: { resId: employee?.id },
            }
        );
        const newEmployee = await this.data.read("hr.employee", record.config.resIds);
        return newEmployee[0];
    },

    async selectEmployee() {
        const currentOrderline = this.get_order().get_selected_orderline();
        if (!currentOrderline) {
            return false;
        }
        const currentEmployee = currentOrderline.get_employee();
        const payload = await makeAwaitable(this.dialog, EmployeeList, {
            employee: currentEmployee,
            getPayload: (newEmployee) => currentOrderline.set_employee(newEmployee),
        });

        if (payload) {
            currentOrderline.set_employee(payload);
        } else {
            currentOrderline.set_employee(false);
        }
        return currentEmployee;
    }
})
