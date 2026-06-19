import { Component, useState } from "@odoo/owl";

export class OfferList extends Component {
    static template = "vanilla_js.OfferList";

    static props = {
        offers: {
            type: Object,
            shape: {
                id: Number,
                buyer: String,
                price: Number,
                deadline: Date,
                state: {
                    type: Object,
                    shape: {
                        id: Number,
                        name: String,
                    },
                },
            },
            optional: true,
        },
    };

    setup() {
        this.errorMessage = useState({value:""})
        this.props.offers = useState([
            { id: 1, buyer: "Alice", price: 250000, state: "pending", deadline: new Date("2025-05-01") },
            { id: 2, buyer: "Bob", price: 300000, state: "pending", deadline: new Date("2025-05-15") },
            { id: 3, buyer: "Charlie", price: 275000, state: "pending", deadline: new Date("2025-06-01") },
        ]);
        this.props.offers.state = useState([
            { id: 1, name: "pending" },
            { id: 2, name: "accepted" },
            { id: 3, name: "refused" },
        ]);
    }

    addToOffer() {
        const list = this.props.offers;
        let lastId = Math.max(...list.map((offer) => offer.id));
        if (Number(document.getElementById("price").value) < 0){
            this.errorMessage.value = "Price Value Must be Greater than 0"
            return;
        }
        const todayVal = new Date().toISOString().split('T')[0];
        if (document.getElementById('deadline').value < todayVal){
            this.errorMessage.value = "Deadline cannot be in past"
            return;
        }
        this.props.offers.push({
            id: lastId + 1,
            buyer: document.getElementById("buyer").value,
            price: Number(document.getElementById("price").value),
            deadline: document.getElementById('deadline').value,
            state: document.getElementById("status").value,
        });
        document.getElementById("buyer").value = "";
        document.getElementById("price").value = "";
        document.getElementById("status").value = "pending";
        document.getElementById("buyer").focus();
        this.errorMessage.value = ""
    }

    acceptOffer(offerId) {
        this.props.offers.forEach((offer) => {
            if (offer.id === offerId) offer.state = "accepted";
            else offer.state = "refused";
        });
    }

    refuseOffer(offerId) {
        this.props.offers.forEach((offer) => {
            if (offer.id === offerId) offer.state = "refused";
        });
    }

    removeOffer(offerId) {
        const index = this.props.offers.findIndex((offer) => offer.id === offerId);
        if (index >= 0) {
            this.props.offers.splice(index, 1);
        }
    }

    getBestOffer() {
        const list = this.props.offers;
        let bestPrice = Math.max(...list.map((offer) => offer.price));
        return list.findIndex((offer) => offer.price === bestPrice);
    }

    acceptBestOffer() {
        let bestPriceId = this.getBestOffer()
        if (bestPriceId >= 0) {
            this.acceptOffer(this.props.offers[bestPriceId].id)
        }
    }
}
