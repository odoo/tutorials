import { startInteractions, setupInteractionWhiteList } from "@web/../tests/public/helpers";
import { defineStyle } from "@web/../tests/web_test_helpers";

import { describe, expect, test, manuallyDispatchProgrammaticEvent } from "@odoo/hoot";
import { queryOne } from "@odoo/hoot-dom";

setupInteractionWhiteList("awesome_website.image_comparison");

describe("interaction_dev", () => {
    test("image_comparison exist", async () => {
        defineStyle(/* css */ `* { transition: none !important; }`);
        const { core } = await startInteractions(`
        <section class="s_image_comparison o_image_comparison_horizontal pb64 pt64">
            <div class="o_container_small">
                <div class="o_image_comparison_container position-relative d-grid overflow-hidden">
                    <img src="/web/image/awesome_website.s_image_comparison_01" class="o_image_before img img-fluid object-fit-cover" alt="" loading="lazy" data-mimetype="image/webp"/>
                    <img src="/web/image/awesome_website.s_image_comparison_02" class="o_image_after img img-fluid object-fit-cover" alt="" loading="lazy" data-mimetype="image/webp"/>
                    <input type="range" min="0" max="100" class="o_image_comparison_slider position-absolute"/>
                    <div class="o_image_comparison_handle position-absolute translate-middle rounded-circle pe-none"/>
                </div>
            </div>
        </section>
    `);
        const input = queryOne("input");
        const snippet = queryOne(".o_image_comparison_container");

        expect(core.interactions).toHaveLength(1);

        expect(input).toHaveValue(50);
        expect(snippet).toHaveStyle({ "--slider-position": "50%" });

        input.value = "99";
        await manuallyDispatchProgrammaticEvent(input, "input");

        expect(queryOne(".o_image_comparison_container")).toHaveStyle({
            "--slider-position": "99%",
        });
    });
});
