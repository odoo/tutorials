import { Component, usePlugin, signal } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { ActionPlugin } from "@web/webclient/actions/action_plugin";
import { DashboardItem } from "./dashboard_item";
import { ReportingPLugin } from "./reporting_plugin";
import { dashboardItems } from "./dashboard_items";
import { DialogPlugin } from "@web/core/dialog/dialog_plugin";
import { ConfigurationDialog } from "./configuration_dialog/configuration_dialog";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, ConfigurationDialog };
    items = dashboardItems.items
    action = usePlugin(ActionPlugin)
    reporting = usePlugin(ReportingPLugin);
    dialog = usePlugin(DialogPlugin)

    disabledItems = signal(
        window.localStorage.getItem("disabledDashboardItems")?.split(",") || []
    );

    openCustomersKanbanView() {
        this.action.doAction("base.action_partner_form", {
            viewType: "kanban",
        });
    }

    openLeadsView() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All Leads",
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]]
        })
    }


    openConfigDialog() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items(),
            disabledItems: this.disabledItems(),
            onUpdateConfiguration: this.updateConfiguration.bind(this)
        })
    }

    updateConfiguration(newDisabledItems) {
        this.disabledItems.set(newDisabledItems);
        window.localStorage.setItem("disabledDashboardItems", newDisabledItems);
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

