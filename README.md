# `Xopy Proxy Rotator`
---
> **`XOPY`**: A lightweight and powerful proxy rotation tool for who need to dynamically manage and rotate proxies.
> Xopy automatically loads, tests, and rotates proxies while setting system-wide configurations. This tool is built to fit seamlessly into your workflow without unnecessary noise, just results...

---

## `Features`
- **```Dynamic Proxy Loading:```** _Easily load proxies from a local file._
- **```Automatic Proxy Testing:```** _Every proxy is tested before rotation, only valid proxies are used._
- **```System-wide Proxy Setting:```** _Automatically apply proxies at the system level for HTTP and HTTPS requests (Currently only for Linux)._
- **```Smooth Proxy Cycling:```** _Randomly rotate through working proxies to avoid detection and maintain anonymity._
- **```Interactive Commands:```** _Simple command interface for rotating proxies, clearing settings, or checking current IP information._

---

## `Requirements`
- Python 3.x
- `requests` _library_ (`pip install requests`)
- `colorama` _library_ (`pip install colorama`)
- `readline` _library_ **(Linux/macOS)** or `pyreadline` **(Windows)**

---

## `Installation`

**1. Clone the repo:**
   ```bash
   git clone https://github.com/1hehaq/xopy.git && cd xopy
   ```

**2. Install requirements:**
   ```bash
   pip3 install -r requirements.txt
   ```
**3. Run xopy:**
  ```bash
  python3 xo.py
  ```

---

## `Usage`

**Load Proxies:**
<br>
<br>
_xopy loads proxies from a file in SOCKS5, SOCKS4, or HTTP format. For fresh daily proxies, check out [`proxies`](https://github.com/TheSpeedX/PROXY-List) and use their list with xopy._

### Commands
```bash
  r - Rotate to next proxy
  c - Clear current proxy
  i - Show current IP
  q - Quit the program
```

---

## `Example Workflow`

**1. Load your proxy list:**
   ```
   [→] Enter the path to your proxy list file: proxies.txt
   ```

**2. After loading, Xopy will test the proxies. Example output:**
   ```
   [‼] Testing 120 proxies, Take a deep breathe..

   [↯] Progress: 67/120
       ↪ Found 45 new working proxies.
       ↪ Total working proxies: 60
   ```

**3. Enter the rotation interface:**
   ```
   [→] Enter command (r/c/i/q): r
   [✓] System proxy set to: 123.45.67.89:8080
   [⏔] Current IP: 123.45.67.89
   ```

**4. Rotate proxies, clear settings, or check your IP with simple commands.**

---

## System-wide Proxy
> _xopy applies proxies system-wide using the `HTTP_PROXY` and `HTTPS_PROXY` environment variables. If you're using xopy within a script or tool that respects these environment variables, the proxy rotation will apply automatically.
To reset your system proxy to default, use the `c` command in the xopy interface._

---

## Proxy File Format
**Your proxy list should contain one proxy per line in the following format:**
```
IP:PORT
```
**For SOCKS proxies, use:**
```
socks4://IP:PORT
socks5://IP:PORT
```

**Example:**
```
123.45.67.89:8080
socks5://111.222.333.444:1080
```

----

> [!WARNING]  
> xopy is only for ethical purposes!
