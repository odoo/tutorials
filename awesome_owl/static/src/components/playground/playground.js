/** @odoo-module **/

import { Component, useEffect, useState } from "@odoo/owl";
import { Counter } from "../counter/counter";
import { Card } from "../card/card";
import { TodoList } from "../todo/todolist/todolist";

export class Playground extends Component {
    static template = "awesome_owl.Playground";
    static components = { Counter, Card, TodoList }
    static props = {}

    setup() {
        super.setup();
        this.state = useState({ counters: 2, sum: 2 });
        
        useEffect(() => {
            this.state.sum += this.state.counters;
        },()=>[this.state.counters]);

        this.cards = [
            {
                title: "Discover the Stars",
                body: "Explore the mysteries of the universe and learn about constellations and galaxies.",
                visit: "<a href='https://nasa.gov' target='_blank'>https://nasa.gov</a>"
            },
            {
                title: "Healthy Living Tips",
                body: "Simple and effective ways to improve your health and boost your energy every day.",
                visit: "<a href='https://www.healthline.com' target='_blank'>https://www.healthline.com</a>"
            },
            {
                title: "Travel on a Budget",
                body: "Find out how to see the world without breaking the bank — travel smart and save money.",
                visit: "<a href='https://www.nomadicmatt.com' target='_blank'>https://www.nomadicmatt.com</a>"
            },
            {
                title: "Mastering JavaScript",
                body: "Step-by-step guide to becoming proficient in JavaScript and building dynamic web apps.",
                visit: "<a href='https://javascript.info' target='_blank'>https://javascript.info</a>"
            },
            {
                title: "Cooking Made Easy",
                body: "Delicious and quick recipes for busy people who love home-cooked meals.",
                visit: "<a href='https://www.budgetbytes.com' target='_blank'>https://www.budgetbytes.com</a>"
            },
            {
                title: "Mindfulness & Meditation",
                body: "Learn techniques to reduce stress and enhance your mental wellbeing through mindfulness.",
                visit: "<a href='https://www.headspace.com' target='_blank'>https://www.headspace.com</a>"
            }
        ];
    }

    incrementSum() {
        this.state.sum++;
    }
}
