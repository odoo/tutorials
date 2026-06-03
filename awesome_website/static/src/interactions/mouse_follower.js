import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

export class MouseFollower extends Interaction {
    static selector = "#wrapwrap";

    dynamicSelectors = {
        ...this.dynamicSelectors,
        _highlighter: () => this.highlighter,
    }

    dynamicContent = {
        _root: {
            "t-on-pointermove": this.debounced(this.onPointerMove, 5),
        },
        _highlighter: {
            "t-att-style": () => ({
                top: `${this.my}px`,
                left: `${this.mx}px`,
            }),
        },
    };

    setup() {
        this.mx = 0;
        this.my = 0;
        this.highlighter = document.createElement("div");
        this.highlighter.classList.add("x_mouse_follower");
    }

    start() {
        this.insert(this.highlighter);
    }

    onPointerMove(ev) {
        this.mx = ev.clientX;
        this.my = ev.clientY;
    }
}

registry.category("public.interactions").add("awesome_website.mouse_follower", MouseFollower);
