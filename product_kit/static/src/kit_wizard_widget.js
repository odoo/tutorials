import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

class KitWizardWidget extends Component {
    setup() {
        this.actionService = useService("action");
    }
    
    openKitWizard() {
        const orderLineId = this.props.record.resId;  // Get sale.order.line ID

        this.actionService.doAction({
            name: "Kit Wizard",  
            type: "ir.actions.act_window",
            res_model: "sub.product.wizard",
            views: [[false, 'form']],
            target: "new",
            context: { 'default_sale_order_line_id': orderLineId }
        });
    }
}

KitWizardWidget.template = "product_kit.KitWizardWidget";
registry.category("fields").add("kit_wizard_widget", { component: KitWizardWidget });
