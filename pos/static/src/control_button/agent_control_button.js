import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalesAgentButton } from "../select_sales_agent_button/select_sales_agent_button";
import { patch } from "@web/core/utils/patch";

patch(ControlButtons, {
    setup() {
        this._super();
    },
    components: {
        ...ControlButtons.components,
        SelectSalesAgentButton,
    }
});
