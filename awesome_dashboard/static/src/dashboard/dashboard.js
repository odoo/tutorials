/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { LazyComponent } from "@web/core/assets";
import { browser } from "@web/core/browser/browser";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { Dialog } from "@web/core/dialog/dialog";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { PieChart } from "../pie_chart/pie_chart";
import { DashboardItem } from "./dashboard_item/dashboard_item";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.dashboard";
    static components = { Layout, DashboardItem, PieChart, LazyComponent }
    async setup() {
        super.setup();
        this.display = {
            controlPanel: {},
        };
        this.action = useService("action");
        this.statistics = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.state = useState({
            uncheckedItems: browser.localStorage.getItem("uncheckedItems")?.split(",") || [],
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "All leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"],
            ],
        });
    }

    openConfigurations() {
        this.dialog.add(DashboardConfiguration, {
            items: this.items,
            uncheckedItems: this.state.uncheckedItems,
            update: this.update.bind(this),
        });
    }

    update(updatedUncheckedItems) {
        this.state.uncheckedItems = updatedUncheckedItems;
    }
}

class DashboardConfiguration extends Component {
    static template = "awesome_dashboard.dashboard_configuration";
    static components = { Dialog, CheckBox };
    static props = ["close", "items", "uncheckedItems", "update"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.uncheckedItems.includes(item.id),
            }
        }));
    }

    done() {
        const updatedUncheckedItems = this.items.filter((i) => !i.enabled).map((i) => i.id);
        browser.localStorage.setItem("uncheckedItems", updatedUncheckedItems);
        this.props.update(updatedUncheckedItems);
        this.props.close();
    }

    update(ev, item) {
        item.enabled = ev.target.checked;
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
