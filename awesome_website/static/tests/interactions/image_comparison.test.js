import { expect, manuallyDispatchProgrammaticEvent, queryOne, test } from "@odoo/hoot";
import { defineStyle } from "@web/../tests/web_test_helpers";
import { setupInteractionWhiteList, startInteractions } from "@web/../tests/public/helpers";

setupInteractionWhiteList("awesome_website.image_comparison");

test("image comparison slider moves", async () => {
    defineStyle(/* css */`* { transition: none !important; }`);
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
    expect(core.interactions).toHaveLength(1);
    expect("input").toHaveStyle({ "--slider-position": "50%" });
    const input = queryOne("input");
    input.value = "5";
    await manuallyDispatchProgrammaticEvent(input, "input");
    expect("input").toHaveStyle({ "--slider-position": "5%" });
});
