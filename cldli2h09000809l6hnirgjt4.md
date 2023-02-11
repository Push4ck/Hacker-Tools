# Titan Stealer: A Sophisticated Golang-Based Information Stealer Malware with Advanced Features

Threat actors promote Titan Stealer, a new Golang-based information stealer virus, on their Telegram channel.

"The stealer can steal a wide range of information from infected Windows machines, including credential data from browsers and crypto wallets, FTP client details, screenshots, system information, and grabbed files," Uptycs security researchers Karthickkumar Kathiresan and Shilpesh Trivedi [wrote](https://www.uptycs.com/blog/titan-stealer-telegram-malware-campaign) in a recent report.

Will Thomas (@BushidoToken), a cybersecurity researcher, discovered the ransomware in November 2022 by querying the IoT search engine Shodan.

Titan is a builder, that allows clients to customize the malware binary to incorporate specific functionality and the type of data to be exfiltrated from a victim's workstation.

When executed, the malware uses a technique known as process hollowing to inject the malicious payload into the memory of a legitimate process called AppLaunch.exe, which is the Microsoft .NET ClickOnce Launch Utility.

Titan Stealer targets popular web browsers such as Google Chrome, Mozilla Firefox, Microsoft Edge, Yandex, Opera, Brave, Vivaldi, 7 Star Browser, Iridium Browser, and others. Armory, Atomic, Bytecoin, Coinomi, Edge Wallet, Ethereum, Exodus, Guarda, Jaxx Liberty, and Zcash are among the crypto wallets mentioned.

It can also collect a list of installed apps on the infected host and data linked with the Telegram desktop app.

The gathered data is then sent as a Base64-encoded archive file to a remote server under the attacker's control. Furthermore, the malware includes a web panel through which enemies can view the stolen data.

The particular method of distribution is unknown at this time, although threat actors have usually employed a variety of ways, including phishing, malicious advertisements, and cracked software.

Thank you for reading our blog today. We hope you found the information helpful and informative. If you enjoyed this blog, be sure to follow us on [**Twitter**](https://twitter.com/areyysharma), [**Instagram**](https://www.instagram.com/official_cyber_hub/), [**Linkedin**](https://www.linkedin.com/in/technical-human/), [**GitHub**](https://github.com/pushkarsharma23), [**Website**](https://officialcyberhub.wixsite.com/cyberhub), and [**Youtube**](https://www.youtube.com/@OfficialCyberHub) for more interesting content and updates. If you have any questions or comments, please feel free to reach out to us. We would love to hear from you. Don't forget to share this with your friends and family who may also find this information useful. Thank you for your support and stay tuned for more!