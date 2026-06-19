import { Component, useState } from "@odoo/owl";

export class Formatter extends Component {
    static template = "vanilla_js.Formatter"

    setup() {
        this.output = useState({ value: 0 });
    }

    get input() {
        return document.getElementById('input').value
    }

    format(ev) {
        if (ev.keyCode === 13 && ev.target.value) {
            const value = this.input;
            if (!value) return "";
            const lastThree = value.slice(-3)
            const remaining = value.slice(0, -3)
            const final = remaining > 0 ? remaining.replace(/\B(?=(\d{2})+(?!\d))/g, ",") + "," + lastThree : lastThree
            let label = ""
            if (Number(this.input) > 1000000000000) {
                label = `${(Number(this.input) / 1000000000000).toFixed(2)} Trillions`
            }
            else if (Number(this.input) > 1000000000) {
                label = `${(Number(this.input) / 1000000000).toFixed(2)} Billions`
            }
            else if (Number(this.input) > 10000000) {
                label = `${(Number(this.input) / 10000000).toFixed(2)} Crores`
            } else if (Number(this.input) > 100000) {
                label = `${(Number(this.input) / 100000).toFixed(2)} Lakhs`
            }
            this.output.value = label ? final + "    " + `(${label})` : final
        }
    }

}
