import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectEmployeeButton } from "../SelectEmployeeButton/SelectEmployeeButton";

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
    },

    get employee() {
        return this.pos.get_order()?.get_selected_orderline()?.get_employee();
    }
})

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectEmployeeButton,
    },
});
