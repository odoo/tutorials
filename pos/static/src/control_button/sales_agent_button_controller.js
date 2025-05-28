import { registry } from "@web/core/registry";
import { SelectSalesAgentButton } from "../select_sales_agent_button/select_sales_agent_button";

// Register the Sales Agent button in the OrderWidgetControlButtons registry
registry.category("point_of_sale.custom_control_buttons").add("select_sales_agent", {
    component: SelectSalesAgentButton,
    position: "left",
    condition: () => true, // Always show this button
});
