# Jetson Orin Nano Super: Boot from NVMe SSD Setup Guide

> Prepared 2026-02-23 for Paul. Reference this when the Jetson arrives.

---

## Prerequisites Checklist

- [ ] NVMe SSD ready (must be **PCIe NVMe**, NOT SATA)
- [ ] Good USB-C cable
- [ ] microSD card (32GB+) as backup for Track B
- [ ] Ubuntu 22.04 x86_64 Desktop ISO downloaded (for UTM)
- [ ] JetPack 6.2 SD card image downloaded as backup
- [ ] **DisplayPort** cable/adapter (the dev kit does NOT have HDMI)
- [ ] USB keyboard and mouse
- [ ] [NVIDIA Developer account](https://developer.nvidia.com/) created

---

## Track A: SDK Manager via UTM (Ideal if it works)

### 1. Create UTM VM

- Select **"Emulate"** (NOT "Virtualize" — Virtualize on Apple Silicon gives ARM64, not x86_64)
- Architecture: **x86_64**
- OS: **Ubuntu 22.04 Desktop** ISO
- RAM: **8GB**
- Storage: **60GB**
- CPU cores: **4**

### 2. Enable USB Sharing

In UTM VM settings, ensure QEMU backend is selected with USB sharing enabled.

### 3. Install NVMe SSD

Insert into the **M.2 slot on the underside** of the carrier board. Secure with the provided screw.

### 4. Put Jetson in Recovery Mode

1. Short **pins 9 and 10** on the **12-pin button header** (NOT the 40-pin GPIO header)
2. Connect USB-C cable from Jetson to Mac
3. Plug in power supply
4. **Keep the jumper on for the entire flash process** — only remove after flashing completes

### 5. Pass USB Through to VM

In UTM, attach the "NVIDIA Corp. APX" USB device to the VM when prompted.

### 6. Verify Detection in VM

```bash
lsusb
```
Look for `NVIDIA Corp. APX`. If it doesn't appear, USB passthrough failed — switch to Track B.

### 7. Install SDK Manager

```bash
sudo apt update && sudo apt upgrade -y
# Download the .deb from https://developer.nvidia.com/sdk-manager inside the VM
sudo apt install ./sdkmanager_*_amd64.deb
sdkmanager
```

### 8. Configure SDK Manager

- Log in with NVIDIA Developer account
- Select: **Jetson Orin Nano (8GB Developer Kit)**
- JetPack version: **JetPack 6.2** (or latest 6.x)
- **Deselect** "Host Machine" (saves space)
- Target storage: **NVMe**
- Setup mode: **Manual Setup** (since already in recovery mode)

### 9. Flash

Click Flash. Wait for completion (~20-60 min). Do NOT disconnect USB or power.

### 10. Post-Flash

1. Remove the jumper from pins 9/10
2. Connect monitor (DisplayPort), keyboard, mouse
3. Power cycle the Jetson
4. Complete Ubuntu OEM setup (username, password, etc.)

### 11. Verify

```bash
lsblk
```
`/dev/nvme0n1p1` should be mounted as `/`.

---

## Track B: microSD First, Then Migrate (Reliable Fallback)

Use this if Track A fails on USB passthrough. No VM needed at all.

### 1. Flash microSD Card (on Mac)

- Download JetPack 6.2 SD card image from [NVIDIA Getting Started](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)
- Flash using [Etcher](https://etcher.balena.io/) — works natively on Mac

### 2. Boot from microSD

1. Insert both microSD and NVMe SSD into the Jetson
2. Connect DisplayPort monitor, keyboard, mouse
3. Power on — boots from microSD
4. This automatically updates the QSPI firmware
5. Complete initial setup (username, password, etc.)

### 3. Clone to NVMe

```bash
# Verify NVMe is detected
lsblk

# Clone microSD to NVMe (takes a while depending on card size)
sudo dd if=/dev/mmcblk0 of=/dev/nvme0n1 bs=4M status=progress

# Update boot config to point to NVMe
sudo nano /boot/extlinux/extlinux.conf
# Change:  root=/dev/mmcblk0p1  →  root=/dev/nvme0n1p1
```

### 4. Reboot from NVMe

1. Shut down the Jetson
2. Remove the microSD card
3. Power on — should boot from NVMe

### 5. Verify

```bash
lsblk
```
`/dev/nvme0n1p1` should be mounted as `/`.

---

## Track C: Nuclear Option

If both tracks fail, borrow a native x86 Ubuntu machine (friend's PC, cheap used PC) and use SDK Manager from there. This is the most reliable method per community consensus.

---

## Key Mistakes to Avoid

| Mistake | Correct Approach |
|---|---|
| Using "Virtualize" in UTM on Apple Silicon | Use **"Emulate"** to get x86_64 |
| Shorting pins on the 40-pin GPIO header | Use the **12-pin button header** |
| Removing jumper before flash completes | Keep jumper on **during entire flash** |
| Using a SATA SSD | Must be **PCIe NVMe** |
| Expecting HDMI output | Dev kit uses **DisplayPort** only |
| Using Ubuntu 24.04 | Stick with **Ubuntu 22.04** for JetPack 6.x |

---

## USB Passthrough Warning (Apple Silicon + UTM)

UTM x86 emulation on Apple Silicon has known USB passthrough limitations. From UTM docs:

> "Due to the way macOS/iOS handles USB capturing (without custom kernel drivers), it is not possible to get a proper hardware reset on the connected device."

If `lsusb` in the VM doesn't show the Jetson, don't waste time debugging — go straight to Track B.

---

## Post-Setup: Enable Max Performance

Once booted from NVMe and everything is working:

```bash
sudo nvpmodel -m 0
sudo jetson_clocks
```

This enables MAXN SUPER mode for maximum performance.

---

## Sources

- [NVIDIA Jetson Orin Nano User Guide - Software Setup](https://developer.nvidia.com/embedded/learn/jetson-orin-nano-devkit-user-guide/software_setup.html)
- [NVIDIA Flashing Support Docs (L4T r36.4.3)](https://docs.nvidia.com/jetson/archives/r36.4.3/DeveloperGuide/SD/FlashingSupport.html)
- [NVIDIA Getting Started Guide](https://developer.nvidia.com/embedded/learn/get-started-jetson-orin-nano-devkit)
- [NVIDIA Forums - Boot from NVMe](https://forums.developer.nvidia.com/t/jetson-orin-nano-developer-kit-boot-from-nvme/250744)
- [NVIDIA Forums - Orin Nano Super NVMe via VM](https://forums.developer.nvidia.com/t/jetson-orin-nano-super-boot-from-nvme-using-a-vm-to-configure-this/318827)
- [Cytron - SDK Manager & NVMe Guide](https://www.cytron.io/tutorial/upgrade-jetson-orin-nano-to-super-using-nvidia-sdk-manager)
- [Jetson Orin Nano Super Guide (GitHub)](https://github.com/ajeetraina/jetson-orin-nano-super-guide)
- [UTM USB Sharing Docs](https://docs.getutm.app/guest-support/sharing/usb/)
