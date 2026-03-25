import { Component, useState } from "@odoo/owl"
import { Dialog } from "@web/core/dialog/dialog";

export class Configuration extends Component{
    static template = "awesome_dashboard.Configuration";
    static components = { Dialog };
    static props = {
        items: {
            type: Array,
        },
        disabledItems: {
            type: Array,
        },
        update: {
            type: Function,
        },
        close: {
            type: Function,
        },
    }

    setup(){
        console.log(this.props.disabledItems);
    }

    onChange(itemId){
        if(this.props.disabledItems.includes(itemId)){
            this.props.disabledItems = this.props.disabledItems.filter(id => id !== itemId);
        }
        else{
            this.props.disabledItems= [...this.props.disabledItems, itemId];
        }
        this.props.update(this.props.disabledItems);
    }
}
