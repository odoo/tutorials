import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item"
import { DashboardItemDialog } from "./dash_item_dialog/dashboard_items_dialog";

export class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {
        Layout,
        DashboardItem
    }

    setup() {
        this.items = useState(useService("dashboard_items").getUsedItems());
        this.action = useService("action")
        this.stats = useState(useService("statistics").loadStatistics());
        this.dialog = useService("dialog");
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']]
        })
    }

    openItemsDialog() {
        this.dialog.add(DashboardItemDialog)
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
