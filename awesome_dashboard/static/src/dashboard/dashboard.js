/** @odoo-module **/

import { _t } from "@web/core/l10n/translation";
import { Layout } from "@web/search/layout"
import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

import { DashboardItem } from "./dashboard_item/dashboard_item";
import { NumberCard } from "./dashboard_item/cards/number_card";
import { PieChartCard } from "./dashboard_item/cards/pie_chart_card";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = { Layout, DashboardItem, NumberCard, PieChartCard, Dialog }

    setup() {
        this.action = useService("action");
        this.statisticsService = useService("awesome_dashboard.statistics");

        this.statistics = useState(this.statisticsService);

        this.items = registry.category("awesome_dashboard").getAll();

        this.state = useState({
            disabledItems:  browser.localStorage.getItem("disabledDashboardItems")?.split(",") || []
        });

        this.dialogService = useService("dialog");
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: "All leads",
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems;
    }

    openDialog() {
        this.dialog = this.dialogService.add(ConfigurationDialog, {
            title: _t("Dashboard items configuration"),
            contentHeader: _t("Which cards do you want to see ?"),
            items: this.items,
            disabledItemsIds: this.state.disabledItems,
            updateConfiguration: (newDisabledItems) => this.updateConfiguration(newDisabledItems)
        });
    }
}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = { Dialog, CheckBox }

    static props = {
        title: { type: String, optional: true },
        contentHeader: { type: String, optional: true },
        items: Object,
        disabledItemsIds: Object,
        updateConfiguration: Function,
        close: { type: Function }
    }

    static defaultProps = {
        title: _t("Dashboard items configuration"),
        contentHeader: _t("Which cards do you want to see ?"),
    }

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItemsIds.includes(item.id)
            }
        }));
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
    }

    onApply() {
        const disabledItems = this.items.filter((item) => !item.enabled).map((item) => item.id);

        browser.localStorage.setItem("disabledDashboardItems", disabledItems);

        this.props.updateConfiguration(disabledItems);

        this.props.close();
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
