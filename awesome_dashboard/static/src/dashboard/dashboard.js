/** @odoo-module **/

import { Component, onMounted, useState, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { browser } from "@web/core/browser/browser";
import { DashboardItem } from "./dashboard_item/dashboard_item";
import { settingDialog } from "./setting_dialog/setting_dialog";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem };

    setup() {
        const initial_card_preference = JSON.parse(browser.localStorage.getItem("user_card_preference"));
        this.action = useService("action");
        this.statisticsService = useService("statisticsService");
        this.dialog = useService("dialog");
        this.state = useState({
            response: this.statisticsService.response,
            card_preference: initial_card_preference && initial_card_preference.length > 0 ? initial_card_preference : [],
        });

        this.intervalId = null;
        this.items = registry.category("awesome_dashboard").get("awesome_dashboard.dashboard");

        onMounted(() => {
            this.intervalId = this.statisticsService.startInterval();
        })

        onWillUnmount(() => {
            if (!this.intervalId) return;
            clearInterval(this.intervalId);
        })
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: "Leads",
            res_model: "crm.lead",
            views: [
                [false, "list"],
                [false, "form"]
            ],
            target: "current",
        });
    }

    savePreference(selectedPreference, close) {
        this.state.card_preference.splice(0, this.state.card_preference.length, ...selectedPreference);
        browser.localStorage.setItem("user_card_preference", JSON.stringify(this.state.card_preference));
        close();
    }

    openSettings() {
        this.dialog.add(settingDialog, {
            apply: this.savePreference.bind(this)
        });
    }
}

registry.category("lazy_components").add("awesome_dashboard.dashboard", AwesomeDashboard);
