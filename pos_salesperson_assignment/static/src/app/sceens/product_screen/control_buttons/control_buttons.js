import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalespersonButton } from "./select_salesperson_button/select_salesperson_button";

export class SalespersonControlButtons extends ControlButtons {
    static components = { 
        ...ControlButtons.components, 
        SelectSalespersonButton 
    };
}
