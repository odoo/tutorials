import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalespersonButton } from "@pos_salesperson/control_buttons/select_salesperson_button/select_salesperson_button";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons, {
    components: { ...ControlButtons.components, SelectSalespersonButton },
});

patch(ControlButtons.prototype, {
    get salesperson() {
        return this.pos.get_order()?.get_salesperson();
    },
});
