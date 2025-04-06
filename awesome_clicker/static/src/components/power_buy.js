import { Component, xml } from "@odoo/owl"
import { useClicker } from "./clicker_hook";

export class PowerBuy extends Component {
    static props = {};
    static template = xml`
        <h1>Power multiplier</h1>
        <div t-if="clicks.level >= 3">
            <div>
                <t t-esc="clicks.power"/>x 
                <i class="fa-solid fa-pizza-slice"/>
            </div>
            <div>
                <button class="btn btn-primary" t-att-disabled="!(this.clicks.clicks>=50000)" t-on-click="incrementPower">Buy Power Multiplier(50000 clicks)</button>
            </div>
        </div>
    `;

    setup(){
        this.clicks = useClicker();
    }

    incrementPower(){
        this.clicks.incrementPower(1);
    }


}