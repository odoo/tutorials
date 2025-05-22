/** @odoo-module **/

import { Component, useState, useEffect } from "@odoo/owl";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { AwesomeDashboardItem } from "@awesome_dashboard/dashboard/dashboard_item";
import { registry } from "@web/core/registry";
import { CogMenu } from "@web/search/cog_menu/cog_menu";
import { AwesomeDashboardConfigDialog } from "@awesome_dashboard/dashboard/dialogs/dashboard_config_dailog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, AwesomeDashboardItem, CogMenu };

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard_statistics"));
        const config = JSON.parse(localStorage.getItem("awesome_dashboard_config"));
        const data = registry.category("awesome_dashboard").get("data");
        this.setActives(config, data);
        this.items = useState({ data });
        this.dialog = useService("dialog");
    }

    onClickCustomers() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Customers",
            target: "current",
            res_model: "res.partner",
            views: [[false, "kanban"]],
        });
    }

    onClickLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "list"]],
        });
    }

    setActives(ref, toUpdate) {
        for (const key in ref) {
            const entry = ref[key];
            const dataItem = toUpdate[key];
            if (dataItem) {
                dataItem.active = entry.active;
            }
        }
    }

    openConfiguration() {
        this.dialog.add(AwesomeDashboardConfigDialog, {
            onConfirm: (configItems) => {
                this.setActives(configItems, this.items.data);
            },
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.AwesomeDashboard", AwesomeDashboard);
