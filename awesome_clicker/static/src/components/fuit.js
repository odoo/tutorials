import { Component, xml } from "@odoo/owl";
import { useClicker } from "./clicker_hook";

export class Fruits extends Component {
    static props = {};
    static template = xml`
        <h1>Fruits</h1>
        <div t-if="clicks.level >= 3">
            <div>
                <t t-esc="clicks.fruits.pear"/>x 
                <span>pear</span>
                <i class="fa fa-tree"/>
            </div>
        </div>
        <div t-if="clicks.level >= 3">
            <div>
                <t t-esc="clicks.fruits.cherry"/>x 
                <span>cherry</span>
                <i class="fa fa-tree"/>
            </div>
        </div>
    `;

    setup() {
        this.clicks = useClicker();
    }
}