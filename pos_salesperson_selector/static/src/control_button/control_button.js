import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { SelectSalespersonButton } from "../select_salesperson_button/select_salesperson_button";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalespersonButton,
    },
});

patch(ControlButtons.prototype, {
    get salesperson() {
        return this.pos.get_order()?.getSalesperson();
    },
});
