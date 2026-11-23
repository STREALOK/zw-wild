# Privacy

zw-wild collects no data and sends nothing anywhere.

- A wild page or living painting stores one flag per page in the viewer's own browser (localStorage key `zw-wild-photosensitivity-ok:` followed by the page's path) to remember that the photosensitivity warning was accepted on that page. Wild widgets store nothing and ask every time. Nothing else is stored, and the flag never leaves the browser.
- The diagram widget loads the open-source mermaid library from esm.sh. If that fails, it tries a local copy at `../devtools/vendor/mermaid/mermaid.min.js` beside the widget file, if one is there.
- The plugin runs no code by itself. In the directory version Claude runs no code for it either: it builds wild files by copying the included Markdown blocks. The folder and uploaded versions carry a small Python tool that runs locally only when the user asks, through the normal permission prompts.

Questions: https://github.com/STREALOK/zw-wild/issues
