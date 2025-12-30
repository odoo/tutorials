import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout"
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { DashboardItemsConfigurationDialog, EXCLUDE_FIELDS_KEY } from "./dashboard_items_configuration_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics")
        this.dialog = useService("dialog")
        this.state = useState(this.statisticsService.state)
        this.excludeItems = useState({value: JSON.parse(localStorage.getItem(EXCLUDE_FIELDS_KEY)) || []})
        this.items = registry.category("awesome_dashboard").get("awesome_dashboard.items")
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads Entries",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]]
        })
    }

    openDashboardItemsConfigurationDialog() {
        this.dialog.add(
            DashboardItemsConfigurationDialog,
            {
                items: this.items,
                setExcludeItems: (items) => {
                    this.excludeItems.value = items
                }
            }
        )
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard)
