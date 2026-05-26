import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { PieChart } from "./pie_chart/pie_chart";
import { GearMenu } from "./gear_menu/gear_menu";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.awesomedashboard";
    static components = { Layout, DashboardItem, PieChart };

    setup() {
        this._t = _t;
        this.action = useService("action");
            this.dialog = useService("dialog");
        this.displayProps = {
            controlPanel: {},
        }
        this.statisticsService = useService("awesome_dashboard.statistics_service");
        this.stats = useState(this.statisticsService.stats);
        // console.log(this.statisticsService);
        this.items = registry.category("awesome_dashboard").getAll();
        console.log(this.items);
        let raw = browser.localStorage.getItem("dashboard.disabled_items");
        let disabled;
        if (raw) {
            disabled = raw.split(",");
        } else {
            disabled = [];
        }
        console.log(disabled);
        this.state = useState({
            disabledItems: disabled, 
        });
    }

    get itemsList() {
        let allowed = [];
        for (let i = 0; i < this.items.length; i++) {
            console.log("Registered Item ID:", this.items[i].id);
            if (!this.state.disabledItems.includes(this.items[i].id)) {
                allowed.push(this.items[i]);
            }
        }
        return allowed;
    }

    openConfiguration() {
        this.dialog.add(GearMenu, {
            items: this.items,
            disabled: this.state.disabledItems,
            onUpdate: this.updateConfig.bind(this),
        });
    }

    updateConfig(newItems) {
        this.state.disabledItems = newItems;
        browser.localStorage.setItem("dashboard.disabled_items", newItems.join(","));
    }

    clickPie(sizeLabel) {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: `${this._t("Orders")} - ${sizeLabel}`,
            res_model: "sale.order", 
            // domain: [["size", "=", sizeLabel.toLowerCase()]],
            views: [
                [false, "list"],
                [false, "form"],
            ],
            target: "new",
        });
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            target: "new",
            views: [
                [false, "list"],
                [false, "form"],
            ],  
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
