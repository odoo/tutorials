import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

class CursorFollow extends Interaction {
    static selector = "#wrapwrap";
    dynamicContent = {
        _root: {
            "t-on-mousemove": (event) => {
                this.x_mouse_follower = event.clientX;
                this.y_mouse_follower = event.clientY;
            },
        },
        ".x_mouse_follower": {
            "t-att-style": () => ({
                position: "absolute",
                "z-index": "auto",
                top: `${this.y_mouse_follower}px`,
                left: `${this.x_mouse_follower}px`,
            }),
        },
    };

    setup() {
        this.x_mouse_follower = 0;
        this.y_mouse_follower = 0;

        this.cursorEl = document.createElement("span");
        this.cursorEl.classList.add("x_mouse_follower");
    }

    start() {
        this.insert(this.cursorEl, this.el);
    }
}

// registry
//     .category("public.interactions")
//     .add("awesome_website.cursor_follow", CursorFollow);
