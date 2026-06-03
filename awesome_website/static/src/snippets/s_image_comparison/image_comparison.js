import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

export class ImageComparison extends Interaction {
    static selector = ".s_image_comparison";

    dynamicContent = {
        ".o_image_comparison_slider": {
            "t-on-input": this.debounced(this.onSliderSlide, 5)
        },
        ".o_image_comparison_container": {
            "t-att-style": () => ({
                "--slider-position": this.sliderPosition,
            }),
        },
    };

    setup() {
        this.sliderPosition = "50%";
    }

    onSliderSlide() {
        let value = document.querySelector(".o_image_comparison_slider").value;
        this.sliderPosition = `${value}%`;
    }
}

registry.category("public.interactions").add("awesome_website.image_comparison", ImageComparison);
