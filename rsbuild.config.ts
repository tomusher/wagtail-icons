import { defineConfig } from "@rsbuild/core";
import { pluginReact } from "@rsbuild/plugin-react";

export default defineConfig({
    source: {
        entry: {
            main: "./src/wagtail_icons/static_src/index.js",
        },
    },
    output: {
        distPath: {
            root: "src/wagtail_icons/static/",
        },
        filenameHash: false,
    },
    dev: {
        writeToDisk: true,
    },
    plugins: [pluginReact()],
});
