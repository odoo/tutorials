import { Component, onWillStart, useState, onMounted } from "@odoo/owl";
import { Layout } from "@web/search/layout"
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboardItem/dashboard_item";
import { rpc } from "@web/core/network/rpc";
import { Piechart } from "./piechart/piechart";
import { MyDialog } from "./mydialog/mydialog";
import { browser } from "@web/core/browser/browser";


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";

    static components = {
        DashboardItem,
        Layout,
        Piechart,
        MyDialog
    }
    setup() {
        this.action = useService("action")
        this.caching = useService("myCaching")
        this.statistics = useState({})
        this.items = registry.category("awesome_dashboard").get("items");
        this.dialog = useService("dialog")
        this.state = useState({
            disabledItems: JSON.parse(browser.localStorage.getItem("disabledDashboardItems")?.split(",") || "{}")
        })

        onWillStart(async () => {
            const stats = await this.caching.loadStatistics()
            Object.assign(this.statistics, await stats());
        })
        onMounted(() => {
            setInterval(async () => {
                const stats = await this.caching.loadStatistics()
                Object.assign(this.statistics, await stats());
            }, 5000)
        })
    }

    _updateConfiguration(newDisabledItems) {
        this.state.disabledItems = newDisabledItems
        console.log(this.state.disabledItems.average_quantity)
        console.log(this.items[0])
    }

    openConfiguration() {
        this.dialog.add(MyDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            updateConfiguration: this._updateConfiguration.bind(this),
        })
    }

    kanban_action() {
        this.action.doAction("base.action_partner_form")
    }

    leads_action() {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'crm action',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }
}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
