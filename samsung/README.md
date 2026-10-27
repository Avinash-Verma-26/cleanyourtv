# Refab Home for Samsung (Tizen)

A custom home screen for a Samsung Tizen TV, set up for a Samsung UN65CU7000 (2023). It is a copy of
[Skylight](https://github.com/SaudSatopay/skylight-tizen) by Saud Satopay (MIT, see
`LICENSE-skylight`, upstream commit in `.skylight-upstream`), changed in three ways:

- The top row is Netflix, YouTube, HBO Max, Peacock and Prime Video. They are found by the name the
  TV gives them (`favouriteNames` in `home/js/catalog.js`), because their package ids differ by region.
- A plain theme: a dark background with no scenery (`theme: 'plain'` in the catalog; `'scenery'`
  brings Skylight's painted sky back).
- macOS scripts: `tools/build.sh` and `tools/fetch-icons.py`.

Samsung doesn't let any app replace its own home. This app comes back about a second after the Home
button, and Samsung's home stays underneath. Skylight was tested on a 2025 TV (Tizen 9); a 2023 TV
runs Tizen 7, so the first install is also the test.

The rest of this repo (`tools/`, `launcher/`) is for Android TVs and doesn't apply to a Samsung.

## Preview on the Mac

```sh
python3 -m http.server 8765 --directory samsung/home
```

Open http://localhost:8765 and use the arrow keys. The preview shows stand-in apps.

## Install on the TV, from a Mac on the same Wi-Fi

1. **Developer Mode.** On the TV, open Apps and type 1 2 3 4 5 on the remote. Turn Developer Mode on
   and set Host PC IP to the Mac's IP. Unplug the TV for a full minute, then plug it back in.
2. **Apps2Samsung CLI.** Download the macOS CLI from
   [Apps2Samsung releases](https://github.com/Apps2Samsung/Apps2Samsung/releases) (the macOS
   `tar.gz` for your Mac's chip), unpack it, and check it finds the TV:
   `./apps2samsung-cli scan`. The binaries are unsigned, so macOS may block the first run: allow it
   under System Settings > Privacy & Security.
3. **Logos and package.**
   ```sh
   python3 -m pip install Pillow
   python3 samsung/tools/fetch-icons.py
   samsung/tools/build.sh
   ```
4. **Install.** The first install opens a browser to sign in to Samsung and make a certificate.
   `--partner` is needed for the helper that brings the home screen back.
   ```sh
   ./apps2samsung-cli install samsung/dist/RefabHome.wgt --tv <TV IP> --partner --launch
   ```
5. **TV settings.** In Start Screen Option (Settings > All Settings > General & Privacy on 2023
   models), keep Start with Smart Hub Home on and turn off Autorun Samsung TV Plus.

To open the home screen when the TV turns on, Skylight uses two SmartThings rules
(`tools/smartthings-skylight.ps1`, Windows PowerShell; see `startup-investigation.md`).

## Undo

Uninstall Refab Home from the TV's Apps settings, and turn Developer Mode off from the same
1 2 3 4 5 screen. Nothing of Samsung's is disabled or removed.
