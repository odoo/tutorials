import { ControlButtons } from "@point_of_sale/static/src/app/screens/product_screen/control_buttons/control_buttons";
import { patch } from "@web/core/utils/patch";
import { SelectSalespersonButton } from "../select_salesperson_button/select_salesperson_button";

patch(ControlButtons.prototype, "custom_pos_buttons", {
    components: {
        ...ControlButtons.components,
        SelectSalespersonButton,
    }
})
