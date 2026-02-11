import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./DashboardItem/dashboardItem";
import { PieChart } from "./PieChart/pieChart";
import { dashboardRegistry } from "./dashboard_registry";
import { Dialog } from "@web/core/dialog/dialog";


class SettingsDialog extends Component {
    static template = "awesome_dashboard.config";
    static components = { Dialog };
    static props = {
        items: { type: Array },
        hiddenItems: { type: Object },
        onApply: { type: Function },
    };

    setup() {
        this.localHidden = useState(
            new Set(this.props.hiddenItems || [])
        );
        this.toggleItem = this.toggleItem.bind(this);
        this.apply = this.apply.bind(this);
    }


    toggleItem(id, checked) {
        if (checked) {
            this.localHidden.delete(id);
        } else {
            this.localHidden.add(id);
        }

        // force reactivity refresh
        this.localHidden = new Set(this.localHidden);
    }


    apply() {
        this.props.onApply([...this.localHidden]);
        this.props.close();
    }
}


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this.action = useService("action");
        this.statistics = useService("statistics");
        this.dialog = useService("dialog");
        this.state = useState(this.statistics);
        this.items = dashboardRegistry.getAll();
        const saved = JSON.parse(
            localStorage.getItem("awesome_dashboard.hidden_items") || "[]"
        );
        this.hiddenItems = useState(new Set(saved));
        // onWillStart(data);
        // setInterval(data,10000);
    }

    viewCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    createLead() {
        this.action.doAction({
            type: "ir.actions.act_window",
            target: "current",
            res_model: "crm.lead",
            views: [[false, "form"]],
        });
    }

    openConfig() {
        this.dialog.add(SettingsDialog, {
            title: "Dashboard Settings",
            items: this.items,
            hiddenItems: [...this.hiddenItems],
            onApply: (hiddenIds) => this.applyHiddenItems(hiddenIds),
        });
    }

    applyHiddenItems(hiddenIds) {
        this.hiddenItems.clear();
        hiddenIds.forEach(id => this.hiddenItems.add(id));
        localStorage.setItem(
            "awesome_dashboard.hidden_items",
            JSON.stringify(hiddenIds)
        );
    }
}


// registry.category("actions").add("awesome_dashboard.dashboard", AwesomeDashboard);
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
