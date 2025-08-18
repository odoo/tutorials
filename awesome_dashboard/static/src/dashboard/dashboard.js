/** @odoo-module **/

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "@awesome_dashboard/dashboard/dashboard_item/dashboard_item";
import { PieChart } from "@awesome_dashboard/dashboard/pie_chart/pie_chart";
import { NumberCard } from "@awesome_dashboard/dashboard/number_card/number_card";
import { PieChartCard } from "@awesome_dashboard/dashboard/pie_chart_card/pie_chart_card";
import { ConfigDialog } from "@awesome_dashboard/dashboard/config_dialog/config_dialog";
import { _t } from "@web/core/l10n/translation";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart, NumberCard, PieChartCard, ConfigDialog}


    setup() {
        this.action = useService("action")
        this.statService = useService("awesome_dashboard.statistics")
        this.stats = useState(this.statService)
        this.dialog = useService("dialog");
        const removedItems = localStorage.getItem("removedItems")?.split(",") ?? [];
        this.items = useState(registry.category("awesome_dashboard").getAll()
            .map((item) => ({
                ...item,
                isSelected: !removedItems.includes(item.id),
            }))
        );

    }

    _t(...args) {
        return _t(...args);
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form")
    }

    openLeads() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: _t('CRM Leads'),
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    openConfiguration() {
        this.dialog.add(ConfigDialog, {
            items: this.items.map((item) => ({
                id: item.id,
                description: item.description,
                isSelected: item.isSelected,
            })),
            apply: (removedIds) => {
                localStorage.setItem("removedItems", removedIds?.join(","));

                this.items.forEach((item) => {
                    item.isSelected = !removedIds.includes(item.id);
                });
            }
        })
    }
}


registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
