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
            root: "src/wagtail_icons/static/wagtailicons/",
            js: "js",
            css: "css",
        },
        filenameHash: false,
    },
    dev: {
        writeToDisk: true,
    },
    performance: {
        chunkSplit: {
            strategy: "all-in-one",
        },
    },
    plugins: [pluginReact()],
});
