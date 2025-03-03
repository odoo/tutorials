import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalespersonButton } from "../select_salesperson_button/select_salesperson_button";

patch(ControlButtons, {
  setup() {
    this._super();
  },
  components: {
    ...ControlButtons.components,
    SelectSalespersonButton,
  },
});
