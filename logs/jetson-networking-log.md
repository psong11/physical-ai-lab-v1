# Jetson Networking Setup — Feb 28, 2026

## Jetson Access Methods
- **USB SSH:** `ssh paul@192.168.55.1` (requires USB cable)
- **WiFi SSH:** `ssh paul@192.168.0.224` (works without USB)
- **Hostname:** changed to `jetson` via `sudo hostnamectl set-hostname jetson`
- **mDNS:** `ssh paul@jetson.local` — not tested yet (may need reboot or Avahi troubleshooting)
- **Display:** no VNC — getting a DisplayPort cable instead

## IP Address Reference (from `hostname -I`)
- `192.168.0.224` — WiFi/LAN (use this)
- `192.168.55.1` — USB device mode
- `172.17.0.1` — Docker bridge (ignore)

## VNC Attempt (abandoned)
- Vino: not available on JetPack r36.5
- x11vnc: not in ARM repos
- TigerVNC: installed but session crashed on startup (xstartup issue)
- **Cleaned up:** uninstalled tigervnc, removed `~/.vnc/`
- **Decision:** use DisplayPort cable for GUI access

## Key Port Numbers
- 22 = SSH, 5900 = VNC, 80 = HTTP, 443 = HTTPS
