# SignPath — черновик заявки (НЕ ОТПРАВЛЯТЬ)

> **Статус:** черновик для просмотра. Никуда не подано.  
> Подавать: https://signpath.io/open-source / https://about.signpath.io/product/open-source-community

---

## Project name

**YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL** (YVP Clipper)

## Repository

- **URL:** https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV
- **License:** GNU GPL v3.0-or-later (copyleft)
- **Default branch:** `main`
- **Latest release:** https://github.com/NeyroslopInzh/YOUTUBE-DLYA-VASHNIH-PEREGOVOROV/releases

## Description

Desktop application (Windows + Linux) for downloading **only selected segments** of YouTube videos as MP4, using yt-dlp and ffmpeg.

Optional **Chromium browser extension** (Load unpacked only — no Chrome Web Store) talks to the desktop app via local HTTP bridge (`127.0.0.1:8766`) and `yvp://` protocol handler.

## Why code signing

Windows SmartScreen shows **“Unknown publisher”** for unsigned `YVPClipper-Setup.exe` and portable exe. We distribute via GitHub Releases only; no store, no paid cert budget.

SignPath would let users install without SmartScreen friction while staying fully open source.

## Artifacts to sign

| Artifact | Platform |
|----------|----------|
| `YVPClipper-Setup.exe` | Windows installer (Inno Setup) |
| `YVPClipper.exe` (portable long-name exe) | Windows portable |
| Optional: Linux binary | Lower priority (no Authenticode) |

## Build reproducibility

- **CI:** GitHub Actions workflow `.github/workflows/release-builds.yml`
- **Trigger:** git tag `v*`
- **Windows build:** Python 3.12 + PyInstaller + Inno Setup (choco)
- **Source of truth:** tag on `main`, public workflow logs

## Release process

1. Tag `vX.Y.Z` on `main`
2. CI builds portable + installer
3. `softprops/action-gh-release` publishes to GitHub Releases
4. *(If SignPath approved)* CI submits build to SignPath → signed artifacts attached to release

## Security / trust

- No telemetry, no auto-update phone-home
- Extension only talks to `localhost:8766`
- `yvp://` registered per-user (HKCU), not machine-wide admin
- GPL — source always public

## Contact (fill before submit)

- **Maintainer name:** _[твоё имя / NeyroslopInzh]_
- **Email:** _[email для SignPath]_
- **Country:** _[страна]_

## Checklist before real submission

- [ ] README clearly states GPL and project purpose
- [ ] LICENSE file present (GPL-3.0)
- [ ] Releases built from public CI on tagged commits
- [ ] No secrets in repo
- [ ] SignPath Open Source policy read: https://about.signpath.io/product/open-source-community
- [ ] Decide: SignPath Foundation vs SignPath.io tier

## Notes

- **Self-signed cert** — бесплатно, но SmartScreen всё равно орёт
- **SignPath** — бесплатно для одобренных OSS, реальная Authenticode-подпись
- После подписи репутация SmartScreen набирается постепенно (не мгновенно)

---

*Черновик создан для внутреннего review. Не отправлять без проверки контактов и политики SignPath.*
