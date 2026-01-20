import { patch } from "@web/core/utils/patch";
import { ControlButtons } from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import { SelectSalesPersonButton } from "../salesperson_button/salesperson_button";

patch(ControlButtons, {
  setup() {
    super.setup();
  },
  components: {
    ...ControlButtons.components,
    SelectSalesPersonButton,
  },
});
