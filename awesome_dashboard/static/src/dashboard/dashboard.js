/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Layout } from "@web/search/layout";
import { Component, useState, reactive } from "@odoo/owl";
import { DashboardItem } from "../dashboard_item/dashboard_item";
import { PieChart } from "../pie_chart/pie_chart";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    setup() {
        this.action = useService("action");
        this.stats = useState(useService("awesome_dashboard.statistics"));
        this.items = registry.category("awesome_dashboard").getAll();
        this.dialog = useService("dialog");
        this.config = useState(this.loadConfig());
    }

    openCustomerKanban() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: "ir.actions.act_window",
            name: _t("Leads"),
            res_model: "crm.lead",
            views: [[false, "list"], [false, "form"]],
        })
    }

    openSettingsDialog() {
        this.dialog.add(ConfigDialog, {
            items: this.items.map(item => ({
                id: item.id,
                title: item.description,
                show: this.config[item.id],
            })),
            updateItemCallback: (itemId, show) => {
                this.config[itemId] = true && show;
            },
        });
    }

    loadConfig() {
        const saveConfig = () => {
            localStorage.setItem("awesome_dashboard.config", JSON.stringify(config));
        }
        let config = JSON.parse(localStorage.getItem("awesome_dashboard.config")) || (() => {
            let tmp = {};
            for (let item of this.items) {
                tmp[item.id] = true;
            }
            return tmp;
        })();
        config = reactive(config, saveConfig);
        saveConfig();
        return config;
    }

    static components = { Layout, DashboardItem, PieChart };
}


class ConfigDialog extends Component {
    static template = "awesome_dashboard.ConfigDialog";

    static props = {
        items: { type: Array, element: {
            id: String,
            title: String,
            show: Boolean,
        } },
        updateItemCallback: { type: Function },
    }

    setup() {
        this.items = useState(
            this.props.items.map(item => ({
                ...item,
            }))
        );
        this.toggleState = this.toggleState.bind(this);
    }

    toggleState(item) {
        item.show = !item.show;
        this.props.updateItemCallback(item.id, item.show);
    }

    static components = { Dialog, CheckBox };
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
