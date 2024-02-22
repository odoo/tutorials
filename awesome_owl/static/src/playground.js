/** @odoo-module **/

import { Component, markup, useState } from "@odoo/owl";

import { Counter } from "./counter";
import { Card } from "./card";
import { TodoList } from "./todo_list";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Card, Counter };
}

// export class Playground extends Component {
//     static template = "awesome_owl.playground";

//     static components = { Card };

//     setup() { 
//         this.state = useState({sum: 2});
//     }

//     incrementSum() {
//         this.state.sum++;
//     }
// }
