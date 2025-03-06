import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons"
import { patch } from "@web/core/utils/patch";

patch(ControlButtons.prototype, {
    setup() {
        super.setup();
    },

    get salesperson() {
        return this.pos.get_order()?.get_salesperson();
    }
});
