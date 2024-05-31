/** @odoo-module **/

import {Component, onMounted, onPatched, onWillStart, reactive, useState} from "@odoo/owl";
import {Layout} from "@web/search/layout";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {DashboardItem} from "./dashboard_item/dashboard_item";
import {PieChart} from "./piechart/piechart";
import {PieChartCard} from "./piechart_card/piechart_card";
import {NumberCard} from "./number_card/number_card";
import {Dialog} from "@web/core/dialog/dialog";
import {CheckBox} from "@web/core/checkbox/checkbox";
import {browser} from "@web/core/browser/browser";

class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    static components = {Layout, DashboardItem, PieChart, NumberCard};

    setup() {
        this.items = [];
        this.display = {
            controlPanel: {},
        };
        this.dialog = useService("dialog");
        this.state = useState({
            disabledItems: browser.localStorage.getItem("disabledItems")?.split(",") || [],
        })
        this.myact = useService("action");
        this.myservice = useState(useService("awesome_dashboard.statistics"));
        this.myservice.pexec=this.filldata;
        console.log("started dashboard");
    }

    filldata(){
        const {orders_by_size,isReady, ...rest}=this.myservice.stats;
        this.result = rest;
        this.orderSize = orders_by_size;

        for (const item in this.result) {
            this.items.push({
                id: item,
                description: item + "Description",
                Component: NumberCard,
                props: {
                    size: 2,
                    title: item,
                    val: this.result[item]
                },
            })
        }
        this.items.push({
                id: this.orderSize,
                description: "Tshirt ordred by size",
                Component: PieChartCard,
                props: {
                    size: 2,
                    label: "Tshirt ordred by size",
                    data: this.orderSize,
                },
            }
        )
    }

    openConfig() {
        this.dialog.add(ConfigurationDialog, {
            items: this.items,
            disabledItems: this.state.disabledItems,
            onUpdateConf: this.updateConf.bind(this),
        })
    }

    updateConf(disabledItems) {
        this.state.disabledItems = disabledItems;
    }

    openCustomers() {
        this.myact.doAction("base.action_partner_form");
    }

    openCrm() {
        this.myact.doAction({
            type: 'ir.actions.act_window',
            name: 'Lead',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

}

class ConfigurationDialog extends Component {
    static template = "awesome_dashboard.ConfigurationDialog";
    static components = {Dialog, CheckBox};
    static props = ["close", "items", "disabledItems", "onUpdateConf"];

    setup() {
        this.items = useState(this.props.items.map((item) => {
            return {
                ...item,
                enabled: !this.props.disabledItems.includes(item.id),
            }
        }));
    }

    done() {
        this.props.close();
    }

    onChange(checked, changedItem) {
        changedItem.enabled = checked;
        const newDisabledItems = Object.values(this.items).filter(
            (item) => !item.enabled
        ).map((item) => item.id)

        browser.localStorage.setItem(
            "disabledItems",
            newDisabledItems,
        );

        this.props.onUpdateConf(newDisabledItems);
    }

}

registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);

