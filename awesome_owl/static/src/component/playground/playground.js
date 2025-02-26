/** @odoo-module **/

const { markup, Component, useState } = owl;
const { Card } = require("../card/card");
const { Counter } = require("../counter/counter");

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };
    content = markup('<div class="text-primary">Content</div>');

    setup() {
        this.sum = useState({
            value: 0,
        });
    }

    incrementSum = () => {
        this.sum.value++;
    }
}
