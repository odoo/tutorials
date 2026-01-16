import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

export class ImageComparison extends Interaction {
    static selector = ".s_image_comparison";

    dynamicContent = {
        ".o_image_comparison_container": {
            "t-att-style": () => ({
                "--slider-position": this.sliderPosition,
            }),
        },
        ".o_image_comparison_slider": {
            "t-on-input": this.onSliderInput,
        }
    };

    setup() {
        this.sliderPosition = "50%";
    }

    destroy() {
        // Reset the slider value to avoid a discrepancy between the slider
        // thumb and the handle.
        this.el.querySelector(".o_image_comparison_slider").value = 50;
    }

    onSliderInput(ev) {
        let value = ev.currentTarget.value;
        if (this.el.classList.contains("o_image_comparison_vertical")) {
            value = 100 - value;
        }
        this.sliderPosition = `${value}%`;
    }
}

registry.category("public.interactions").add("awesome_website.image_comparison", ImageComparison);
