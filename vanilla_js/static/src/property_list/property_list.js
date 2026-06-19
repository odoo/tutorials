import { Component, useState, useRef } from "@odoo/owl";

export class PropertyList extends Component {
    static template = "vanilla_js.PropertyList";

    static props = {
        items: {
            type: Object,
            shape: {
                id: Number,
                name: String,
                state: {
                    type: Object,
                    shape: {
                        id: Number,
                        name: String,
                    },
                },
                bedrooms: Number,
            },
            optional: true,
        },
    };

    setup() {
        this.nameRef = useRef('name')
        this.stateRef = useRef('state')
        this.bedrooomRef = useRef('bedrooms')
        this.props.items = useState([
            { id: 1, name: "Sunset Villa", state: "new", bedrooms: 3 },
            { id: 2, name: "Ocean Breeze", state: "offer_received", bedrooms: 4 },
            { id: 3, name: "Green Meadows", state: "offer_accepted", bedrooms: 2 },
            { id: 4, name: "City Loft", state: "sold", bedrooms: 1 },
            { id: 5, name: "Mountain Retreat", state: "cancelled", bedrooms: 5 },
        ]);
        this.props.items.state = useState([
            { id: 1, name: "new" },
            { id: 2, name: "offer_received" },
            { id: 3, name: "offer_accepted" },
            { id: 4, name: "sold" },
            { id: 5, name: "cancelled" },
        ])
        this.toggleState = useState({ value: "asc" });
        this.toggleOrder = useState({ value: "id" });
    }

    orderByID() {
        this.toggleState.value = "asc";
        this.toggleOrder.value = "id";
        return this.props.items.sort((a, b) => a.id - b.id);
    }

    orderByName() {
        this.toggleState.value = "asc";
        this.toggleOrder.value = "name";
        return this.props.items.sort((a, b) => a.name.localeCompare(b.name));
    }

    orderByState() {
        this.toggleState.value = "asc";
        this.toggleOrder.value = "state";
        return this.props.items.sort((a, b) => a.state.localeCompare(b.state));
    }

    orderByBedrooms() {
        this.toggleState.value = "asc";
        this.toggleOrder.value = "bedrooms";
        return this.props.items.sort((a, b) => a.bedrooms - b.bedrooms);
    }

    sortBy() {
        if (this.toggleState.value === "asc") this.toggleState.value = "desc";
        else if (this.toggleState.value === "desc") this.toggleState.value = "asc";
        return this.props.items.reverse();
    }

    addToList() {
        const list = this.props.items;
        let lastId = Math.max(...list.map((item) => item.id));
        this.props.items.push({
            id: lastId + 1,
            name: document.getElementById("name").value,
            state: document.getElementById("state").value,
            bedrooms: document.getElementById("bedrooms").value,
        });
        document.getElementById("name").value = "";
        document.getElementById("state").value = "new";
        document.getElementById("bedrooms").value = "";
        document.getElementById("name").focus();
    }

    removeItem(itemId) {
        const index = this.props.items.findIndex((item) => item.id === itemId)
        if (index >= 0) {
            this.props.items.splice(index, 1)
        }
    }
}
