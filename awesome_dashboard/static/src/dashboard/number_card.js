import { Component, t, useProps } from "@odoo/owl";

export class NumberCard extends Component {
    static template = "awesome_dashboard.NumberCard";

    props = useProps({
        title: t.string(),
        value: t.number()
    });
}