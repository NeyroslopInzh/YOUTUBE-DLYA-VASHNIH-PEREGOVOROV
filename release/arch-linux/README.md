# Arch Linux binary

Бинарник собирается в контейнере `archlinux/archlinux`.

## Если бинарник уже лежит здесь

```bash
sudo pacman -S ffmpeg
chmod +x "YOUTUBE VIDEOS DOWNLOAD FOR VASHNIE PEREGOVORI 2002 KRUTO COOL SOSAL"
./YOUTUBE\ VIDEOS\ DOWNLOAD\ FOR\ VASHNIE\ PEREGOVORI\ 2002\ KRUTO\ COOL\ SOSAL
```

> **ffmpeg обязателен.** Без системного ffmpeg возможен `ffmpeg exited with code -11` (segfault bundled-бинарника).

## Сборка на Arch вручную

```bash
./build_arch_linux.sh
```

## Сборка через GitHub Actions (Arch container)

```bash
gh workflow run build-arch-linux.yml
gh run list --workflow=build-arch-linux.yml
gh run download <RUN_ID> -D release/arch-linux
```

## Сборка через WSL (после установки Ubuntu + перезагрузки)

```bat
build_arch_linux_wsl.bat
```
