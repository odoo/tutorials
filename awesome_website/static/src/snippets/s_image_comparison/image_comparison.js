import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

export class ImageComparison extends Interaction {
    static selector = ".o_image_comparison_container";

    dynamicContent = {
        ".o_image_comparison_slider": {
            "t-on-input": this.updateSliderPosition,
        },
    };

    updateSliderPosition(event) {
        this.el.style.setProperty("--slider-position", `${event.target.value}%`);
    }
}

registry.category("public.interactions").add("awesome_website.image_comparison", ImageComparison);
