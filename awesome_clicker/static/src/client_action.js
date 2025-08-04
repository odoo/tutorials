/** @odoo-module **/

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useClicker } from "./clicker_service";
import { ClickValue } from "./click_value";

export class ClickerClientAction extends Component {
    static template = "awesome_clicker.ClientAction";
    static components = { ClickValue };
    static props = ["*"];

    setup() {
        this.clicker = useClicker();
    }

    onIncrement10Click() {
        this.clicker.increment(10);
    }
    
    onIncrement1000Click() {
        this.clicker.increment(1000);
    }
    
    onTestClick() {
        this.clicker.increment(10000000); // Add 10 million for testing
    }
    
    onBuyClickBot() {
        this.clicker.buyClickBot();
    }
    
    onBuyBigBot() {
        this.clicker.buyBigBot();
    }
    
    onBuyPower() {
        this.clicker.buyPower();
    }
    
    onBuyQuantumBot() {
        this.clicker.buyQuantumBot();
    }
    
    onBuySpecialBot() {
        this.clicker.buySpecialBot();
    }
    
    onReset() {
        if (confirm("Are you sure you want to reset all progress? This cannot be undone!")) {
            this.clicker.reset();
        }
    }
    
    get canBuyClickBot() {
        return this.clicker.state.clicks >= 1000;
    }
    
    get canBuyBigBot() {
        return this.clicker.state.clicks >= 5000;
    }
    
    get canBuyPower() {
        return this.clicker.state.clicks >= 50000;
    }
    
    get canBuyQuantumBot() {
        return this.clicker.state.clicks >= 250000;
    }
    
    get canBuySpecialBot() {
        return this.clicker.state.clicks >= 2000000;
    }
    
}

registry.category("actions").add("awesome_clicker.client_action", ClickerClientAction);
