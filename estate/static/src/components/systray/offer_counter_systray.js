import { Component, useState, useEffect, useRef, onWillUnmount } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { rpc } from "@web/core/network/rpc";

const POLL_INTERVAL_MS = 30_000;
const OFFER_MODEL = "estate.property.offer";
const PENDING_DOMAIN = [["status", "=", false]];
const MAX_BADGE_DISPLAY = 99;

class OfferCounterSystray extends Component {
    static template = "estate.OfferCounterSystray";
    static props = {};

    setup() {
        this.actionService = useService("action");

        this.state = useState({
            count: 0,
            loading: true,
        });

        this._intervalId = null;

        useEffect(
            () => {
                this._fetchOfferCount();

                this._intervalId = setInterval(
                    () => this._fetchOfferCount(),
                    POLL_INTERVAL_MS
                );

                return () => {
                    clearInterval(this._intervalId);
                    this._intervalId = null;
                };
            },
            () => []
        );

        onWillUnmount(() => {
            clearInterval(this._intervalId);
            this._intervalId = null;
        });
    }

    get displayCount() {
        if (this.state.count > MAX_BADGE_DISPLAY) {
            return `${MAX_BADGE_DISPLAY}+`;
        }
        return String(this.state.count);
    }

    async _fetchOfferCount() {
        try {
            const pendingOfferCount = await rpc("/web/dataset/call_kw", {
                model: OFFER_MODEL,
                method: "search_count",
                args: [PENDING_DOMAIN],
                kwargs: {},
            });

            this.state.count = pendingOfferCount;
            this.state.loading = false;
        } catch (fetchError) {
            console.warn("[OfferCounterSystray] fetch failed:", fetchError);
        }
    }

    openOfferList() {
        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Pending Offers",
            res_model: OFFER_MODEL,
            domain: PENDING_DOMAIN,
            views: [[false, "list"], [false, "form"]],
            target: "current",
        });
    }
}

registry.category("systray").add(
    "estate.OfferCounter",
    {
        Component: OfferCounterSystray,
        sequence: 10,
    }
);
