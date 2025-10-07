import { patch } from "@web/core/utils/patch";
import { SalespersonButton } from "../salesperson_button/salesperson_button";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";

patch(ControlButtons.components, {
    SalespersonButton
})
