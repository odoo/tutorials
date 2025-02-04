/** @odoo-module **/

import { Component, useState, } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Layout } from "@web/search/layout";
import { useService } from "@web/core/utils/hooks";
import { DashboardItem } from "./dashboard_item";
import {PieChart} from './PieChart/PieChart'
import { browser } from "@web/core/browser/browser";

import './service/loadStatistics'


class AwesomeDashboard extends Component {
    static template = "awesome_dashboard.AwesomeDashboard";
    
    static components = { Layout, DashboardItem, PieChart};
    
    setup(env) {
        this.EXCLUDED_ITEM_IDS="EXCLUDED_ITEM_IDS"
        
        this.items= registry.category('awesome_dashboard').get('items', [])
        
        this.excluded_item_ids = JSON.parse(browser.localStorage.getItem(this.EXCLUDED_ITEM_IDS) || "[]") 
        
        this.formState=useState({});

        for(let i=0;i<this.items.length;i++) {
            const key= this.items[i].id;
            const value = {isChecked: true ,...this.items[i]};

            if(this.excluded_item_ids.indexOf(key) !=-1) {
                value.isChecked= false
            }

            this.formState[key]= value
            console.log(this.formState[key].id, this.formState[key].isChecked);
        }

        this.display = {
            controlPanel: {},
        };
        this.action= useService("action")

        this.statisticResponse  = useState(useService('awesome_dashboard.statistics')).staticData
    }

    
    updateRpcResponse(data) {
        this.state.rpcResponse= data;
    }

    openCustomers() {
        this.action.doAction("base.action_partner_form");
    }

    openLeads(activity) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            target: 'current',
            res_model: 'crm.lead',
            views: [[false, 'list'], [false, 'form']],
        });
    }

    updateFormState(id) {
        const arr= JSON.parse(browser.localStorage.getItem(this.EXCLUDED_ITEM_IDS) || "[]") 
        
        if(this.formState[id].isChecked) {
            arr.push(id)
            browser.localStorage.setItem(this.EXCLUDED_ITEM_IDS, JSON.stringify(arr)) 
        } else {
            const index = arr.findIndex((item) => item === id);
            if (index >= 0)
                arr.splice(index, 1);

            browser.localStorage.setItem(this.EXCLUDED_ITEM_IDS, JSON.stringify(arr))
        }

        this.formState[id].isChecked= !this.formState[id].isChecked

    }
    
}
registry.category("lazy_components").add("AwesomeDashboard", AwesomeDashboard);
