import { Component, markup, useState } from "@odoo/owl";
import Counter from "./counter/counter";
import Card from "./card/card";

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = { Counter, Card };

    setup() {
      this.state = useState({ sum: 0 });
    }

    incrementSum() {
      this.state.sum++;
    }

    card_content = "<div class='text-primary'>content</div>"
    card2_content = markup("<div class='text-primary'>content</div>")
}
