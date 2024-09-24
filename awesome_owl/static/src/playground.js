/** @odoo-module **/

import {Component, useState} from "@odoo/owl";
import {Counter} from './counter/counter.js'
import {Card} from './card/card.js'
import {TodoList} from './todo/todo_list.js'

export class Playground extends Component {
    static template = "awesome_owl.playground";
    static components = {Counter, Card, TodoList}

    setup() {
        this.state = useState({
            sum: 0,
            counters: Object.fromEntries(
                Array.from({length: 10}, (_, i) => [i, {value: i + 1}])
            )

        });

        // initial sum calculation
        this.updateCounterSum();
    }

    updateCounterSum() {
        this.state.sum = Object.values(this.state.counters).reduce((acc, counter) => acc + counter.value, 0);
    }
}
