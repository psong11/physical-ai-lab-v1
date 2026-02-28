# Jetson Orin Nano Flash Log — Feb 28, 2026

## Summary

Successfully flashed the Jetson Orin Nano with JetPack 6.2 via a ThinkPad T460
running Ubuntu 22.04. The Jetson is now booting from NVMe SSD (238.5 GB) and
accessible over Wi-Fi via SSH.

---

## Hardware Used

| Device | Role |
|--------|------|
| MacBook Pro (Apple Silicon) | Created bootable Ubuntu USB with Etcher |
| ThinkPad T460 | Native x86 Linux machine for SDK Manager + flashing |
| 32GB SanDisk USB drive | Ubuntu 22.04 installer |
| Jetson Orin Nano (8GB) | Target device |
| NVMe SSD (238.5 GB) | Jetson boot drive |

## What Was Installed

| Component | Version |
|-----------|---------|
| Ubuntu (ThinkPad) | 22.04.5 LTS Desktop (amd64) |
| Ubuntu (Jetson) | 22.04.5 LTS (aarch64, tegra kernel 5.15.185) |
| JetPack | 6.2 (L4T R36, Revision 5.0) |
| SDK Manager | Latest .deb from developer.nvidia.com |

## Steps Completed

### 1. Created Bootable USB (on Mac)
- Downloaded `ubuntu-22.04.5-desktop-amd64.iso`
- Flashed to 32GB SanDisk USB using **balenaEtcher** (ARM64 version for Apple Silicon)
- macOS Finder doesn't show the USB after flash — this is normal (Linux partitions)

### 2. Installed Ubuntu on ThinkPad T460
- Booted from USB: power on → **Enter** key for Startup Interrupt Menu → **F12** for Boot Menu
  - F12 alone during boot did NOT work — had to use the Interrupt Menu first
  - Secure Boot was already disabled (check under F1 → BIOS → Security)
  - Had to change **UEFI/Legacy Boot** to **"Both"** (was "UEFI Only")
  - Set boot priority to **UEFI First**
- Selected **"Try or Install Ubuntu"** from GRUB
- Normal installation, checked "Download updates while installing"
- Erased disk and installed Ubuntu
- Post-install: `sudo apt update && sudo apt upgrade -y`

### 3. Installed SDK Manager (on ThinkPad)
- Downloaded `.deb` from https://developer.nvidia.com/sdk-manager in Firefox
- Installed: `sudo apt install ./sdkmanager_*_amd64.deb`
- "Unsandboxed download" warning appeared — this is just a warning, not an error
- SDK Manager does not support `--version` flag; just run `sdkmanager` to verify

### 4. Flashed Jetson
- Put Jetson in recovery mode (jumper on pins 9+10 of 12-pin header)
- Connected USB-C from Jetson to ThinkPad
- Verified with `lsusb` — showed "NVIDIA Corp. APX"
- SDK Manager settings: Jetson Orin Nano, JetPack 6.2, NVMe storage
- Flash completed successfully
- Removed jumper after flash

### 5. First Boot & Setup (Headless via Serial)
- Connected Jetson USB-C to ThinkPad
- On ThinkPad: `ls /dev/ttyACM*` found the serial device
- Connected: `sudo screen /dev/ttyACM0 115200`
- Completed Ubuntu OEM setup (username: paul, hostname: ubuntu)
- Note: `ls /dev/cu.usb*` on Mac did NOT find the serial device — use the ThinkPad

### 6. Verification
- `lsblk`: `/dev/nvme0n1p1` (237G) mounted as `/` — booting from NVMe
- `cat /etc/nv_tegra_release`: R36, Revision 5.0 (JetPack 6.2)
- Connected to Wi-Fi: `sudo nmcli dev wifi connect "SSID" password "PASS"`
- Jetson IP: **192.168.0.224** (check with `hostname -I`, capital I)
- SSH works: `ssh paul@192.168.0.224` from MacBook

## Gotchas & Lessons Learned

1. **ThinkPad T460 boot menu**: F12 alone doesn't work. Press **Enter** first for the Startup Interrupt Menu, then F12.
2. **UEFI/Legacy Boot**: Had to change from "UEFI Only" to "Both" for the USB to boot.
3. **Etcher on Mac**: Download the **ARM64** version for Apple Silicon Macs.
4. **USB not visible in Finder**: Normal after flashing — macOS can't read Linux partitions.
5. **SDK Manager `--version`**: Not a valid flag. Just run `sdkmanager` to confirm it's installed.
6. **Headless Jetson setup**: Use ThinkPad + `screen /dev/ttyACM0 115200`, not Mac.
7. **`hostname -i` vs `hostname -I`**: Lowercase gives loopback (127.0.0.1), capital gives real IPs.

## Current State

```
MacBook Pro ──── development machine, SSH into Jetson
ThinkPad T460 ── Ubuntu 22.04 + SDK Manager (flashing tool, done for now)
Jetson Orin Nano ── JetPack 6.2, NVMe boot, Wi-Fi connected, SSH accessible
```

## What's Next

- Run `sudo apt update && sudo apt upgrade -y` on the Jetson
- Enable max performance: `sudo nvpmodel -m 0 && sudo jetson_clocks`
- Verify CUDA: `nvcc --version`
- Continue with Week 2+ of the master plan (model deployment to Jetson comes in Week 4)
