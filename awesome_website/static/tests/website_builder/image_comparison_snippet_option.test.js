import { describe, expect, test, queryOne, click } from "@odoo/hoot";
import { animationFrame } from "@odoo/hoot-dom";
import {
    defineWebsiteModels,
    setupWebsiteBuilderWithSnippet,
} from "@website/../tests/builder/website_helpers";

describe("awesome_website.builder", () => {
    defineWebsiteModels();

    test("rounding in image_comparison", async () => {
        const { waitSidebarUpdated } = await setupWebsiteBuilderWithSnippet("s_image_comparison");

        const snippetEl = queryOne(":iframe .s_image_comparison");

        await click(snippetEl);
        await waitSidebarUpdated();

        expect("[data-container-title='Image Comparison']").toBeVisible();
        const optionBtn = queryOne("[data-class-action='o_image_comparison_m_rounded']");
        expect(optionBtn).toBeVisible();

        await click(optionBtn);

        await animationFrame();

        expect(snippetEl).toHaveClass("o_image_comparison_m_rounded");
    });
});
