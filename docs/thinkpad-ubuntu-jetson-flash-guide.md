# ThinkPad T460 → Ubuntu 22.04 → Flash Jetson Orin Nano

> Complete step-by-step guide. Zero ambiguity. One-shot.

---

## What You Need In Front of You

- [ ] ThinkPad T460 (plugged into power)
- [ ] 32GB USB thumb drive (will be **erased** — back up anything on it)
- [ ] Jetson Orin Nano with NVMe SSD installed
- [ ] USB-C cable (for connecting Jetson to ThinkPad)
- [ ] Jetson power supply
- [ ] Jumper wire or tweezers (for recovery mode pins)
- [ ] Your MacBook (to create the bootable USB)
- [ ] Wi-Fi or Ethernet available for the ThinkPad

---

## PART 1: Create Bootable USB (On Your Mac)

### Step 1.1 — Download Ubuntu 22.04.5 LTS Desktop ISO

Download this exact file on your Mac:

```
https://releases.ubuntu.com/22.04/ubuntu-22.04.5-desktop-amd64.iso
```

> **Why 22.04 specifically?** NVIDIA SDK Manager officially supports Ubuntu 22.04 (Jammy).
> It does NOT support 24.04 yet. The .5 point release is the latest 22.04 with all
> updates baked in.

The file is ~5 GB. Wait for it to finish completely.

### Step 1.2 — Flash the USB Drive

**Option A: Use Etcher (Easiest — Recommended)**

1. Download and install [balenaEtcher](https://etcher.balena.io/) on your Mac
2. Open Etcher
3. Click **"Flash from file"** → select the `ubuntu-22.04.5-desktop-amd64.iso`
4. Click **"Select target"** → select your 32GB USB drive
5. Click **"Flash!"**
6. Wait for it to complete and verify (~5-10 min)
7. macOS may say "The disk you inserted was not readable" — click **Eject** (this is normal)

**Option B: Use `dd` in Terminal (If Etcher doesn't work)**

```bash
# 1. Insert USB drive into your Mac

# 2. Find your USB drive's disk identifier
diskutil list

# Look for your 32GB drive — it will be something like /dev/disk4
# TRIPLE-CHECK the disk number. Wrong number = erased Mac drive.

# 3. Unmount the USB drive (replace disk4 with YOUR disk number)
diskutil unmountDisk /dev/disk4

# 4. Write the ISO (replace disk4 with YOUR disk number)
#    Use rdisk (raw disk) for faster writes
sudo dd if=~/Downloads/ubuntu-22.04.5-desktop-amd64.iso of=/dev/rdisk4 bs=4m status=progress

# 5. Wait for it to finish (~5-10 min). Do NOT interrupt.

# 6. Eject
diskutil eject /dev/disk4
```

### Step 1.3 — Remove USB from Mac

Safely eject and pull out the USB drive. It's now a bootable Ubuntu installer.

---

## PART 2: Install Ubuntu 22.04 on the ThinkPad T460

### Step 2.1 — Boot from USB

1. **Plug the USB drive** into the ThinkPad
2. **Power on** (or restart) the ThinkPad
3. **Immediately press F12 repeatedly** as it powers on — this opens the Boot Menu
   - If you see the Lenovo logo, you're pressing at the right time
   - If it boots into Windows/whatever is installed, restart and try again
4. In the Boot Menu, select your **USB drive** (it may say "USB HDD" or the drive brand name)
5. Select **"Try or Install Ubuntu"** from the GRUB menu

> **If F12 doesn't work:** Try F1 to enter BIOS Setup → go to "Startup" tab →
> "Boot" → move USB to the top of the boot order → save and exit.
>
> **If Secure Boot blocks it:** Enter BIOS (F1) → Security → Secure Boot →
> set to **Disabled** → save and exit → try F12 again.

### Step 2.2 — Install Ubuntu

When the Ubuntu installer loads:

1. Click **"Install Ubuntu"**
2. **Keyboard layout:** English (US) — or whatever you use
3. **Updates and other software:**
   - Select **"Normal installation"**
   - Check **"Download updates while installing Ubuntu"** (if connected to Wi-Fi/Ethernet)
   - Check **"Install third-party software for graphics and Wi-Fi hardware"**
4. **Installation type:**
   - Select **"Erase disk and install Ubuntu"**
   - This wipes whatever is on the ThinkPad's internal drive — that's what we want
   - Click **"Install Now"** → **"Continue"** to confirm
5. **Time zone:** Select yours
6. **Your name / computer's name / username / password:**
   - Name: `Paul Song` (or whatever you prefer)
   - Computer name: `thinkpad` (keep it simple)
   - Username: `paul`
   - Password: something you'll remember (you'll type it often for `sudo`)
7. **Wait for installation** (~15-30 min)
8. When prompted, click **"Restart Now"**
9. When it says **"Please remove the installation medium"**, pull out the USB drive, then press Enter

### Step 2.3 — First Boot & Updates

You should now boot into a fresh Ubuntu 22.04 desktop. Log in, then open a terminal (Ctrl+Alt+T):

```bash
# Update everything to latest
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y curl wget git build-essential

# Reboot to apply any kernel updates
sudo reboot
```

### Step 2.4 — Connect to the Internet

If Wi-Fi didn't connect automatically:
- Click the network icon in the top-right corner of the desktop
- Select your Wi-Fi network and enter the password

> **ThinkPad T460 Wi-Fi note:** The T460 uses an Intel 8260 Wi-Fi chip which is
> well-supported out of the box on Ubuntu 22.04. It should just work.

---

## PART 3: Install NVIDIA SDK Manager

### Step 3.1 — Create an NVIDIA Developer Account (If You Haven't Already)

Go to https://developer.nvidia.com/ in Firefox (pre-installed on Ubuntu) and create a free account, or log in if you already have one.

### Step 3.2 — Download SDK Manager

1. In Firefox on the ThinkPad, go to: https://developer.nvidia.com/sdk-manager
2. Click **"Download"** (you may need to log in first)
3. Download the **.deb (Ubuntu)** package — it will be named something like `sdkmanager_*_amd64.deb`

### Step 3.3 — Install SDK Manager

```bash
# Navigate to Downloads
cd ~/Downloads

# Install the .deb package (the filename may vary slightly)
sudo apt install ./sdkmanager_*_amd64.deb

# If there are dependency errors, fix them with:
sudo apt --fix-broken install -y

# Verify it installed
sdkmanager --version
```

---

## PART 4: Flash the Jetson Orin Nano

### Step 4.1 — Install the NVMe SSD (If Not Already Done)

Insert the NVMe SSD into the **M.2 slot on the underside** of the Jetson carrier board. Secure with the provided screw.

### Step 4.2 — Put Jetson in Recovery Mode

1. Make sure the Jetson is **powered OFF** and **unplugged**
2. Locate the **12-pin button header** on the carrier board (NOT the 40-pin GPIO header)
3. **Short pins 9 and 10** using a jumper wire or tweezers
   - Pin 9 = FC_REC (Force Recovery)
   - Pin 10 = GND (right next to it)
4. **Keep the jumper connected** — do NOT remove it yet
5. Connect the **USB-C cable** from the Jetson's USB-C port to the ThinkPad's USB port
6. **Plug in the Jetson's power supply**
7. The Jetson is now in recovery mode (no display output — that's expected)

### Step 4.3 — Verify Jetson Is Detected

```bash
lsusb
```

Look for a line containing **`NVIDIA Corp. APX`** — this confirms the Jetson is in recovery mode and the ThinkPad sees it.

If you don't see it:
- Try a different USB port on the ThinkPad
- Try a different USB-C cable
- Re-do the recovery mode steps (unplug power, re-short pins, reconnect)

### Step 4.4 — Launch SDK Manager and Configure

```bash
sdkmanager
```

1. **Log in** with your NVIDIA Developer account
2. On the **Step 01 — Development Environment** screen:
   - **Product Category:** Jetson
   - **Hardware Configuration:** select **Jetson Orin Nano Developer Kit** (the 8GB version)
     - If it says "detected" that's great — it auto-detected your Jetson
   - **Target OS:** JetPack 6.2 (or whatever latest 6.x is offered)
   - **DeSelect "Host Machine"** under additional SDKs — you don't need to install anything on the ThinkPad itself
3. Click **Continue**

### Step 4.5 — Accept License & Download

1. Accept the license agreement
2. SDK Manager will download all necessary components (~15-20 GB depending on what's selected)
3. **This will take a while** depending on your internet speed. Let it finish completely.

### Step 4.6 — Flash

1. When downloads are complete, SDK Manager will ask how to flash
2. Select:
   - **Storage Device:** NVMe
   - **OEM Configuration:** Runtime (this lets you do the initial Ubuntu setup on first boot)
3. You may be prompted for your ThinkPad's `sudo` password — enter it
4. Click **Flash**
5. **Wait for the flash to complete** — this takes ~20-60 minutes
   - Do NOT disconnect the USB cable
   - Do NOT unplug the Jetson's power
   - Do NOT remove the jumper wire yet
   - Do NOT close the lid on the ThinkPad (prevent it from sleeping)

> **Prevent ThinkPad from sleeping during flash:** Go to Settings → Power →
> set "Blank Screen" to **Never**, and turn off "Automatic Suspend".

### Step 4.7 — Flash Complete

Once SDK Manager says flash is complete:

1. **Remove the jumper** from pins 9 and 10 on the Jetson
2. **Disconnect the USB-C cable** from the ThinkPad
3. Connect to the Jetson:
   - **DisplayPort** monitor (NOT HDMI — the dev kit only has DisplayPort)
   - USB keyboard
   - USB mouse
4. **Power cycle** the Jetson (unplug power, wait 5 seconds, plug back in)

### Step 4.8 — Jetson First Boot Setup

The Jetson should boot into the Ubuntu OEM setup screen:

1. Accept the license
2. Select language, keyboard, timezone
3. Create your user account (username, password)
4. Wait for initial setup to complete

### Step 4.9 — Verify Everything Works

Open a terminal on the Jetson:

```bash
# Verify you're booted from NVMe
lsblk
# /dev/nvme0n1p1 should be mounted as /

# Check JetPack version
cat /etc/nv_tegra_release

# Check available disk space
df -h /

# Enable max performance mode
sudo nvpmodel -m 0
sudo jetson_clocks

# Verify CUDA is available
nvcc --version
```

If `lsblk` shows `/dev/nvme0n1p1` mounted as `/` — **you're done. The Jetson is flashed and running from NVMe.**

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| F12 doesn't open Boot Menu | Enter BIOS with F1, change boot order |
| Secure Boot blocks USB boot | Disable Secure Boot in BIOS (F1 → Security) |
| `lsusb` doesn't show NVIDIA APX | Try different USB port, different cable, redo recovery mode |
| SDK Manager can't detect Jetson | Make sure Jetson is in recovery mode AND shows in `lsusb` |
| Flash fails midway | Power cycle Jetson, re-enter recovery mode, try again — the Jetson is safe |
| Downloads are slow | SDK Manager downloads ~15-20 GB; be patient or use Ethernet |
| ThinkPad sleeps during flash | Disable automatic suspend in Settings → Power |
| Jetson boots but no display | Make sure you're using **DisplayPort**, not HDMI |
| Wi-Fi doesn't work on ThinkPad | Run `sudo apt install linux-firmware` and reboot |

---

## Summary of What You'll Have When Done

```
MacBook ─── your development machine (code, SSH into Jetson)
ThinkPad T460 ─── Ubuntu 22.04, SDK Manager (only needed for flashing)
Jetson Orin Nano ─── JetPack 6.2, booting from NVMe, ready for deployment
```

The ThinkPad's main job is done after the flash. You can keep it around for future
re-flashes or JetPack upgrades, but your day-to-day development will be on your
MacBook, SSH-ing into the Jetson.
