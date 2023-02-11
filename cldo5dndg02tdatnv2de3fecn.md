# The Ice Breaker: The New Threat Knocking on the Door of Gaming and Gambling Industry!

The gaming and gambling sectors are under attack and the clock is ticking down to the start of the [**ICE London 2023**](https://www.icelondon.uk.com/) gaming industry trade fair next week. This new attack campaign is unlike anything the industry has ever seen before, employing clever social engineering tactics to deploy a dangerous JavaScript backdoor.

The Israeli cybersecurity company, Security Joes, is on the case, tracking the activity cluster known as the Ice Breaker. The attackers pose as customers with account registration issues and initiate a [**conversation**](https://www.securityjoes.com/post/operation-ice-breaker-targets-the-gam-bl-ing-industry-right-before-it-s-biggest-gathering) with support agents under the guise of needing assistance. But their real intentions become clear when they urge the agent to open a screenshot image hosted on Dropbox.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1675328502693/b9318074-dcd7-4e7b-bfbd-0d41394bf6f6.png align="center")

Clicking the image leads to a payload that retrieves either an LNK or a VBScript file. The former is configured to download and run an MSI package that contains a Node.js implant. This implant is loaded with features that enable the attacker to steal passwords and cookies, take screenshots, run VBScript from a remote server, and even open a reverse proxy on the compromised host.

If the victim executes the VBS downloader, the infection culminates in the deployment of the [**Houdini**](https://malpedia.caad.fkie.fraunhofer.de/details/win.houdini) remote access trojan. The origins of the threat actors are unknown, but they have been observed using broken English in their [**conversations**](https://twitter.com/malwrhunterteam/status/1576984214351724546) with customer service agents.

"We are dealing with a highly skilled threat actor who shows the potential of being sponsored by an interest owner," warns Felipe Duarte, a senior threat researcher at Security Joes. "This new attack vector is highly effective and must not be taken lightly by the gaming and gambling industry."

Don't let the Ice Breaker catch you off guard. Stay ahead of the game and protect your business from this dangerous threat.

Thank you for reading our blog today. We hope you found the information helpful and informative. If you enjoyed this blog, be sure to follow us on [**Twitter**](https://twitter.com/areyysharma), [**Instagram**](https://www.instagram.com/official_cyber_hub/), [**Linkedin**](https://www.linkedin.com/in/technical-human/), [**GitHub**](https://github.com/pushkarsharma23), [**Website**](https://officialcyberhub.wixsite.com/cyberhub), and [**Youtube**](https://www.youtube.com/@OfficialCyberHub) for more exciting content and updates. If you have any questions or comments, please feel free to reach out to us. We would love to hear from you. Don't forget to share this with your friends and family who may also find this information useful. Thank you for your support and stay tuned for more!