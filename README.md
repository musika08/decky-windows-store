# Decky store list for Windows plugins

A static plugin list in the format Decky Loader's store reads, served by GitHub Pages at
`https://musika08.github.io/decky-windows-store/plugins`. It lists Windows-only plugins:

- [Overdrive](https://github.com/musika08/overdrive): ROG Ally controls (performance, Auto TDP, fans, Auto SR).
- [Control Center](https://github.com/musika08/decky-control-center): brightness, volume, Wi-Fi, Bluetooth, battery limit.
- [Clarity](https://github.com/musika08/clarity): per-game OptiScaler with AMD FSR 4 Lite and frame generation.
- [Traction](https://github.com/musika08/traction): ROG Ally controller mode, grip vibration, touchscreen and the Armoury Crate switch.

Each version points at the plugin's own GitHub release zip; Decky checks the zip's SHA-256 before installing.

## Use

Decky Loader for Windows shows this list next to the official store. On another Decky build: Decky settings, Store,
choose **Custom**, and enter the address above.

## Update

Edit `plugins.json` (newest version first), then run `python build_store.py` and commit the regenerated
`plugins/index.html` and `plugins/versions/index.html`.
