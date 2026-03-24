//addons/awesome_owl/static/src/playground/playground.js
import {Component, markup, useState} from "@odoo/owl";
import {Counter} from "../counter/counter";
import {Card} from "../card/card";


export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = {Counter, Card};

    value1 = "<div class='text-primary'>some content</div>"
    value2 = markup("<div>some text 2</div>")

    setup() {
        this.state = useState({sum: 2})
    }

    incrementSum() {
        this.state.sum++;

    }
}


