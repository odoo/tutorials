import { Component, xml } from "@odoo/owl";
import { useClicker } from "./clicker_hook";

export class ClickBot extends Component {
    static props = {};
    static template = xml`
        <h1>Bots</h1>
        <div>
            <div>
                <t t-esc="clicks.clickBots"/>x 
                <span>ClickBots (10 clicks/10 seconds)</span>
                <i class="fa fa-android"/>
            </div>
            <div>
                <button class="btn btn-primary" t-att-disabled="!(this.clicks.clicks>=1000)" t-on-click="incrementClickBot">Buy ClickBot (1000 clicks)</button>
            </div>
        </div>
        <div t-if="clicks.level >= 2">
            <div>
                <t t-esc="clicks.bigBots"/>x 
                <span>BigBot (100 clicks/10 seconds)</span>
                <i class="fa fa-android"/>
            </div>
            <div>
                <button class="btn btn-primary" t-att-disabled="!(this.clicks.clicks>=5000)" t-on-click="incrementBigBot">Buy BigBot (5000 clicks)</button>
            </div>
        </div>
    `;

    setup() {
        this.clicks = useClicker();
    }

    incrementClickBot() {
        this.clicks.incrementClickBots(1);
    }

    incrementBigBot(){
        this.clicks.incrementBigBots(1);
    }
}