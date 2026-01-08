import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

class MouseFollower extends Interaction {
    static selector = "#wrapwrap";
    dynamicSelectors = {
        ...this.dynamicSelectors,
        _followerEl: () => this.followerEl,
    }
    dynamicContent = {
        _root: {
            "t-on-pointermove": this.debounced(this.onPointerMove, 5),
        },
        _followerEl: {
            "t-att-style": () => ({
                top: `${this.yp}px`,
                left: `${this.xp}px`,
            }),
        },
    };

    setup() {
        // Initialize starting position
        this.xp = 0;
        this.yp = 0;

        // Create the Follower
        this.followerEl = document.createElement("div");
        this.followerEl.classList.add("x_mouse_follower");
    }
    start() {
        // Append it to the page. It will be cleaned automatically if the
        // interaction is destroyed.
        this.insert(this.followerEl);
    }

    onPointerMove(ev) {
        const mouseX = ev.clientX;
        const mouseY = ev.clientY;

        this.xp += mouseX - this.xp;
        this.yp += mouseY - this.yp;
    }
}

registry.category("public.interactions").add("awesome_website.mouse_follower", MouseFollower);
