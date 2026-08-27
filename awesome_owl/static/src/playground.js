import { Component, useState } from "@odoo/owl";
import { Counter } from "./counter/counter";
import { Card } from "./card/card";
import { TodoList } from "./todo_list/TodoList";

export class Playground extends Component {
    static template = "awesome_owl.playground";

    static components = { Counter, Card, TodoList};

    setup() {
        /*
        I define the counters here so I can show them as much as I want
        */
        this.state = useState({
            counters_num: 2,
            counters_ref: []
        });
    }

    // It registry the reference of the child here
    registerCounter(id, counterInstance) {
        this.state.counters_ref[id] = counterInstance;
    }

    get sum() {
        return this.state.counters_ref.reduce(
            (acc, counter) => acc + (counter?.state?.value || 0),
            0
        )
    }

}
