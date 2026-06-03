import { Component, xml, useState, onWillStart, onWillDestroy } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

class Timer extends Component {
    static template = xml`<section class="w-25 mx-auto p-8">
        <div class="card">
            <div class="card-body">
                <t t-out="this.state.time.toLocaleString(this.props.locale)"/>
            </div>
        </div>
    </section>`;
    static props = {
        locale: {
            type: String,
        },
    };

    setup() {
        this.state = useState({ time: new Date() });
        onWillStart(() => {
            this.interval = setInterval(() => (this.state.time = new Date()), 100);
        });
        onWillDestroy(() => {
            if (this.interval) {
                clearInterval(this.interval);
            }
        });
    }
}

class OwlInteraction extends Interaction {
    static selector = "main";
    dynamicContent = {
        _root: {
            "t-component": () => [Timer, { locale: "fr" }],
        },
    };
}

registry.category("public_components").add("OwlTimer", Timer);

registry.category("public.interactions").add("OwlTimer", OwlInteraction);
