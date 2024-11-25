/** @odoo-module **/

import { Component, useState} from "@odoo/owl";
import { Dialog } from "@web/core/dialog/dialog";
import { CheckBox } from "@web/core/checkbox/checkbox";
import { browser } from "@web/core/browser/browser";

export class AwesomeDashboardDialog extends Component {
    static template = "awesome_dashboard.AwesomeDashboardDialog";
    static components = { Dialog, CheckBox }
    static props = {
        dashboardItems: Object,
        updateUncheckedItems: Function,
    }
    setup(){
        this.dashboardItems = useState(this.props.dashboardItems);
        this.itemCheckmarks = useState({ });
        let id;
        for(let i = 0; i < this.dashboardItems.length; i++){
            id = this.dashboardItems.at(i).id;
            this.itemCheckmarks[id] = !browser.localStorage.getItem("AwesomeDashboardUncheckedItems").includes(id);
        }
        this.dialogTitle = "Dashboard items configuration";
    }
    itemToggle(ev, id){
        this.itemCheckmarks[id] = ev;
    }
    dialogSave(){
        const newUncheckedItems = [];
        for(let i = 0; i < this.dashboardItems.length; i++){
            if(this.itemCheckmarks[this.dashboardItems.at(i).id] == false){
                newUncheckedItems.push(this.dashboardItems.at(i).id);
            }
        }
        browser.localStorage.setItem("AwesomeDashboardUncheckedItems", newUncheckedItems);
        this.props.updateUncheckedItems(newUncheckedItems);
    }
}
