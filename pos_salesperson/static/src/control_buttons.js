import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalesPersonButton } from "./salesperson_button";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons, {
    components: {
        ...ControlButtons.components,
        SelectSalesPersonButton,
    },

    get salesperson() {
        const temp_salesperson = this.pos.get_order()?.get_salesperson()
        return this.pos.get_order()?.get_salesperson();
        console.log("Default salesperson", temp_salesperson);
    },
});
