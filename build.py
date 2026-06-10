#!/usr/bin/env python3
"""
MITRE ATT&CK 中文本地化构建脚本
从 STIX bundle 提取数据，翻译为中文，生成 JS 数据文件供 HTML 查看器使用
"""
import json
import re
import sys

# ============================================================
# 翻译词典
# ============================================================

# 战术 (Tactics) 翻译
TACTIC_TR = {
    "Reconnaissance": "侦察",
    "Resource Development": "资源开发",
    "Initial Access": "初始访问",
    "Execution": "执行",
    "Persistence": "持久化",
    "Privilege Escalation": "权限提升",
    "Defense Impairment": "防御削弱",
    "Stealth": "隐蔽",
    "Credential Access": "凭证访问",
    "Discovery": "发现",
    "Lateral Movement": "横向移动",
    "Collection": "收集",
    "Command and Control": "命令与控制",
    "Exfiltration": "数据窃取",
    "Impact": "影响",
}

TACTIC_DESC_TR = {
    "Reconnaissance": "攻击者正在收集可用于规划未来行动的信息。侦察包括攻击者主动或被动收集可用于支持目标定位的信息的技术。",
    "Resource Development": "攻击者正在建立可用于支持行动的资源。资源开发包括攻击者创建、购买或窃取/入侵可用于支持目标定位的资源的技术。",
    "Initial Access": "攻击者正在试图进入您的网络。初始访问包括使用各种入口向量在网络中获得初始立足点的技术。",
    "Execution": "攻击者正在试图运行恶意代码。执行包括导致攻击者控制的代码在本地或远程系统上运行的技术。",
    "Persistence": "攻击者正在试图维持其立足点。持久化包括攻击者用于在系统重启、凭据更改和其他可能切断其访问的中断情况下保持对系统访问的技术。",
    "Privilege Escalation": "攻击者正在试图获取更高级别的权限。权限提升包括攻击者用于在系统或网络上获取更高级别权限的技术。",
    "Defense Impairment": "攻击者正在试图破坏安全机制、管道和工具，使防御者无法看到或信任正在发生的事情。防御削弱包括降低、禁用或破坏防御能力的技术。",
    "Stealth": "攻击者正在试图隐藏和掩盖其行为，使其看起来像正常行为。隐蔽包括通过融入合法活动来降低被检测可能性的技术。",
    "Credential Access": "攻击者正在试图窃取账户名和密码。凭证访问包括窃取凭据（如账户名和密码）的技术。使用合法凭据可使攻击者访问系统、更难以被发现，并提供创建更多账户的机会。",
    "Discovery": "攻击者正在试图了解您的环境。发现包括攻击者可用于获取有关系统和内部网络知识的技术。这些技术帮助攻击者观察环境并在决定如何行动之前确定方向。",
    "Lateral Movement": "攻击者正在试图在您的环境中移动。横向移动包括攻击者用于进入和控制网络上远程系统的技术。完成其主要目标通常需要探索网络以找到目标并随后获得访问权限。",
    "Collection": "攻击者正在试图收集对其目标有用的数据。收集包括攻击者可用于收集信息的技术以及信息来源。",
    "Command and Control": "攻击者正在试图与受控系统通信以控制它们。命令与控制包括攻击者可用于与受其控制的系统通信的技术。",
    "Exfiltration": "攻击者正在试图窃取数据。数据窃取包括攻击者可用于从您的网络窃取数据的技术。一旦收集到数据，攻击者通常会在窃取之前对其进行打包以避免检测。",
    "Impact": "攻击者正在试图操纵、中断或破坏您的系统和数据。影响包括攻击者用于破坏可用性或通过操纵业务和运营流程来损害完整性的技术。",
}

# 技术(Techniques)翻译 - 完整词典
TECHNIQUE_TR = {
    # A
    "Abuse Elevation Control Mechanism": "滥用权限提升控制机制",
    "Access Token Manipulation": "访问令牌操纵",
    "Accessibility Features": "辅助功能",
    "Account Access Removal": "账户访问移除",
    "Account Discovery": "账户发现",
    "Account Manipulation": "账户操纵",
    "Acquire Access": "获取访问权限",
    "Acquire Infrastructure": "获取基础设施",
    "Active Scanning": "主动扫描",
    "Additional Cloud Credentials": "添加云凭证",
    "Additional Cloud Roles": "添加云角色",
    "Additional Container Cluster Roles": "添加容器集群角色",
    "Additional Email Delegate Permissions": "添加邮箱委托权限",
    "Additional Local or Domain Groups": "添加本地或域组",
    "Adversary-in-the-Middle": "中间人攻击",
    "AppCert DLLs": "AppCert DLL",
    "AppInit DLLs": "AppInit DLL",
    "Application Access Token": "应用程序访问令牌",
    "Application Layer Protocol": "应用层协议",
    "Application Shimming": "应用程序兼容性垫片",
    "Application Window Discovery": "应用程序窗口发现",
    "Application or System Exploitation": "应用程序或系统利用",
    "Application Deployment Software": "应用程序部署软件",
    "AppDomainManager": "AppDomainManager 劫持",
    "AppleScript": "AppleScript",
    "Archive Collected Data": "归档收集的数据",
    "Archive via Custom Method": "通过自定义方法归档",
    "Archive via Library": "通过库归档",
    "Archive via Utility": "通过工具归档",
    "ARP Cache Poisoning": "ARP 缓存投毒",
    "Artificial Intelligence": "人工智能",
    "AS-REP Roasting": "AS-REP Roasting",
    "Asymmetric Cryptography": "非对称加密",
    "Asynchronous Procedure Call": "异步过程调用(APC)",
    "At": "At (Windows)",
    "At (Linux)": "At (Linux)",
    "Audio Capture": "音频捕获",
    "Audio-Visual Content": "音视频内容",
    "Authentication Package": "身份验证包",
    "AutoHotKey & AutoIT": "AutoHotKey 和 AutoIT",
    "Automated Collection": "自动收集",
    "Automated Exfiltration": "自动窃取",

    # B
    "Backup Software Discovery": "备份软件发现",
    "Bandwidth Hijacking": "带宽劫持",
    "Bash History": "Bash 历史",
    "Bidirectional Communication": "双向通信",
    "Binary Padding": "二进制填充",
    "Bind Mounts": "绑定挂载",
    "BITS Jobs": "BITS 作业",
    "Boot or Logon Autostart Execution": "启动或登录自动执行",
    "Boot or Logon Initialization Scripts": "启动或登录初始化脚本",
    "Bootkit": "Bootkit",
    "Botnet": "僵尸网络",
    "Break Process Trees": "断开进程树",
    "Browser Extensions": "浏览器扩展",
    "Browser Fingerprint": "浏览器指纹",
    "Browser Information Discovery": "浏览器信息发现",
    "Browser Session Hijacking": "浏览器会话劫持",
    "Brute Force": "暴力破解",
    "Build Image on Host": "在主机上构建镜像",
    "Business Relationships": "业务关系",
    "Bypass User Account Control": "绕过用户账户控制(UAC)",

    # C
    "Cached Domain Credentials": "缓存域凭据",
    "Ccache Files": "Ccache 文件",
    "CDNs": "CDN",
    "Change Default File Association": "更改默认文件关联",
    "Chat Messages": "聊天消息",
    "Clear Command History": "清除命令历史",
    "Clear Linux or Mac System Logs": "清除 Linux 或 Mac 系统日志",
    "Clear Mailbox Data": "清除邮箱数据",
    "Clear Network Connection History and Configurations": "清除网络连接历史和配置",
    "Clear Persistence": "清除持久化",
    "Clear Windows Event Logs": "清除 Windows 事件日志",
    "ClickOnce": "ClickOnce",
    "Client Configurations": "客户端配置",
    "Clipboard Data": "剪贴板数据",
    "Cloud Account": "云账户",
    "Cloud Accounts": "云账户",
    "Cloud Administration Command": "云管理命令",
    "Cloud API": "云API",
    "Cloud Accounts": "云账户",
    "Cloud Application Integration": "云应用集成",
    "Cloud Firewall": "云防火墙",
    "Cloud Groups": "云组",
    "Cloud Instance Metadata API": "云实例元数据 API",
    "Cloud Infrastructure Discovery": "云基础设施发现",
    "Cloud Secrets Management Stores": "云密钥管理存储",
    "Cloud Service Dashboard": "云服务控制台",
    "Cloud Service Discovery": "云服务发现",
    "Cloud Service Hijacking": "云服务劫持",
    "Cloud Services": "云服务",
    "Cloud Storage Object Discovery": "云存储对象发现",
    "CMSTP": "CMSTP",
    "Code Repositories": "代码仓库",
    "Code Signing": "代码签名",
    "Code Signing Certificates": "代码签名证书",
    "Code Signing Policy Modification": "代码签名策略修改",
    "Collection": "收集",
    "Command Obfuscation": "命令混淆",
    "Command and Scripting Interpreter": "命令和脚本解释器",
    "Communication Through Removable Media": "通过可移动介质通信",
    "Compile After Delivery": "投递后编译",
    "Compiled HTML File": "编译的 HTML 文件",
    "Component Firmware": "组件固件",
    "Component Object Model": "组件对象模型(COM)",
    "Component Object Model Hijacking": "组件对象模型劫持",
    "Compromise Accounts": "入侵账户",
    "Compromise Hardware Supply Chain": "入侵硬件供应链",
    "Compromise Host Software Binary": "入侵主机软件二进制",
    "Compromise Infrastructure": "入侵基础设施",
    "Compromise Software Dependencies and Development Tools": "入侵软件依赖和开发工具",
    "Compromise Software Supply Chain": "入侵软件供应链",
    "Compression": "压缩",
    "Compute Hijacking": "计算劫持",
    "Conditional Access Policies": "条件访问策略",
    "Confluence": "Confluence",
    "Container Administration Command": "容器管理命令",
    "Container and Resource Discovery": "容器和资源发现",
    "Container API": "容器 API",
    "Container CLI/API": "容器 CLI/API",
    "Container Orchestration Job": "容器编排作业",
    "Container Service": "容器服务",
    "Content Injection": "内容注入",
    "Control Panel": "控制面板",
    "Control Panel Items": "控制面板项",
    "COR_PROFILER": "COR_PROFILER探查器",
    "Create Account": "创建账户",
    "Create Cloud Instance": "创建云实例",
    "Create or Modify System Process": "创建或修改系统进程",
    "Create Process with Token": "使用令牌创建进程",
    "Create Snapshot": "创建快照",
    "Credential API Hooking": "凭证 API 钩子",
    "Credential Stuffing": "凭证填充",
    "Credentials": "凭据",
    "Credentials from Password Stores": "从密码存储获取凭据",
    "Credentials from Web Browsers": "从 Web 浏览器获取凭据",
    "Credentials in Files": "文件中的凭据",
    "Credentials in Registry": "注册表中的凭据",
    "Cron": "Cron",
    "Customer Relationship Management Software": "客户关系管理(CRM)软件",
    "Custom Command and Control Protocol": "自定义命令控制协议",
    "Custom Cryptographic Protocol": "自定义加密协议",

    # D
    "Data Compressed": "数据压缩",
    "Data Destruction": "数据销毁",
    "Data Encoding": "数据编码",
    "Data Encrypted": "数据加密",
    "Data Encrypted for Impact": "加密数据以造成影响",
    "Data from Cloud Storage": "从云存储获取数据",
    "Data from Configuration Repository": "从配置仓库获取数据",
    "Data from Information Repositories": "从信息仓库获取数据",
    "Data from Local System": "从本地系统获取数据",
    "Data from Network Shared Drive": "从网络共享驱动器获取数据",
    "Data from Removable Media": "从可移动介质获取数据",
    "Data Manipulation": "数据操纵",
    "Data Obfuscation": "数据混淆",
    "Data Staged": "数据暂存",
    "Data Transfer Size Limits": "数据传输大小限制",
    "Databases": "数据库",
    "DCSync": "DCSync",
    "Dead Drop Resolver": "死信解析器",
    "Debugger Evasion": "调试器规避",
    "Defacement": "篡改",
    "Default Accounts": "默认账户",
    "Delay Execution": "延迟执行",
    "Delete Cloud Instance": "删除云实例",
    "Deobfuscate/Decode Files or Information": "去混淆/解码文件或信息",
    "Deploy Container": "部署容器",
    "Determine Physical Locations": "确定物理位置",
    "Develop Capabilities": "开发能力",
    "Device Driver Discovery": "设备驱动发现",
    "Device Registration": "设备注册",
    "DHCP Spoofing": "DHCP 欺骗",
    "Digital Certificates": "数字证书",
    "Direct Cloud VM Connections": "直接云虚拟机连接",
    "Direct Network Flood": "直接网络洪泛",
    "Direct Volume Access": "直接卷访问",
    "Disable Crypto Hardware": "禁用加密硬件",
    "Disable or Modify Cloud Firewall": "禁用或修改云防火墙",
    "Disable or Modify Cloud Logs": "禁用或修改云日志",
    "Disable or Modify Cloud Log": "禁用或修改云日志",
    "Disable or Modify Linux Audit System": "禁用或修改 Linux 审计系统",
    "Disable or Modify Linux Audit System Log": "禁用或修改 Linux 审计系统日志",
    "Disable or Modify Network Device Firewall": "禁用或修改网络设备防火墙",
    "Disable or Modify System Firewall": "禁用或修改系统防火墙",
    "Disable or Modify Tools": "禁用或修改工具",
    "Disable or Modify Windows Event Log": "禁用或修改 Windows 事件日志",
    "Disable or Modify Windows Event Logging": "禁用 Windows 事件日志记录",
    "Disabling Security Tools": "禁用安全工具",
    "Disk Content Wipe": "磁盘内容擦除",
    "Disk Structure Wipe": "磁盘结构擦除",
    "Disk Wipe": "磁盘擦除",
    "DLL": "DLL 劫持",
    "DLL Search Order Hijacking": "DLL 搜索顺序劫持",
    "DLL Side-Loading": "DLL 侧加载",
    "DNS": "DNS",
    "DNS Calculation": "DNS 计算",
    "DNS Server": "DNS 服务器",
    "DNS/Passive DNS": "DNS/被动 DNS",
    "Domain Account": "域账户",
    "Domain Accounts": "域账户",
    "Domain Controller Authentication": "域控制器认证",
    "Domain Fronting": "域名前置",
    "Domain Generation Algorithms": "域名生成算法(DGA)",
    "Domain Groups": "域组",
    "Domain or Tenant Policy Modification": "域或租户策略修改",
    "Domain Properties": "域属性",
    "Domain Trust Discovery": "域信任发现",
    "Domains": "域名",
    "Double File Extension": "双文件扩展名",
    "Downgrade Attack": "降级攻击",
    "Downgrade System Image": "降级系统镜像",
    "Drive-by Compromise": "路过式入侵",
    "Drive-by Target": "路过式目标",
    "Dynamic API Resolution": "动态 API 解析",
    "Dynamic Data Exchange": "动态数据交换(DDE)",
    "Dynamic Linker Hijacking": "动态链接器劫持",
    "Dynamic Resolution": "动态解析",
    "Dynamic-link Library Injection": "动态链接库注入",
    "Dylib Hijacking": "Dylib 劫持",

    # E
    "Electron Applications": "Electron 应用程序",
    "Elevated Execution with Prompt": "带提示的提权执行",
    "Email Account": "邮件账户",
    "Email Accounts": "邮件账户",
    "Email Bombing": "邮件轰炸",
    "Email Collection": "邮件收集",
    "Email Forwarding Rule": "邮件转发规则",
    "Email Hiding Rules": "邮件隐藏规则",
    "Email Spoofing": "邮件欺骗",
    "Embedded Payloads": "嵌入载荷",
    "Emond": "Emond事件监控守护进程",
    "Encrypted Channel": "加密通道",
    "Encrypted/Encoded File": "加密/编码文件",
    "Endpoint Denial of Service": "端点拒绝服务",
    "Environmental Keying": "环境密钥",
    "Escape to Host": "逃逸到主机",
    "ESXi Administration Command": "ESXi 管理命令",
    "Establish Accounts": "建立账户",
    "/etc/passwd and /etc/shadow": "/etc/passwd 和 /etc/shadow",
    "Evil Twin": "邪恶双胞胎",
    "Exclusive Control": "独占控制",
    "Executable Installer File Permissions Weakness": "可执行安装程序文件权限弱点",
    "Execution Guardrails": "执行护栏",
    "Exfiltration Over Alternative Protocol": "通过替代协议窃取",
    "Exfiltration Over Asymmetric Encrypted Non-C2 Protocol": "通过非对称加密非C2协议窃取",
    "Exfiltration Over Bluetooth": "通过蓝牙窃取",
    "Exfiltration Over C2 Channel": "通过C2通道窃取",
    "Exfiltration Over Other Network Medium": "通过其他网络介质窃取",
    "Exfiltration Over Physical Medium": "通过物理介质窃取",
    "Exfiltration Over Symmetric Encrypted Non-C2 Protocol": "通过对称加密非C2协议窃取",
    "Exfiltration Over Unencrypted Non-C2 Protocol": "通过非加密非C2协议窃取",
    "Exfiltration Over Web Service": "通过Web服务窃取",
    "Exfiltration Over Webhook": "通过Webhook窃取",
    "Exfiltration to Cloud Storage": "窃取到云存储",
    "Exfiltration to Code Repository": "窃取到代码仓库",
    "Exfiltration to Text Storage Sites": "窃取到文本存储站点",
    "Exfiltration over USB": "通过USB窃取",
    "Exploit Public-Facing Application": "利用面向公众的应用程序",
    "Exploitation for Client Execution": "利用客户端执行",
    "Exploitation for Credential Access": "利用获取凭证",
    "Exploitation for Defense Impairment": "利用削弱防御",
    "Exploitation for Privilege Escalation": "利用提升权限",
    "Exploitation for Stealth": "利用实现隐蔽",
    "Exploitation of Remote Services": "利用远程服务",
    "Exploits": "漏洞利用",
    "Extended Attributes": "扩展属性",
    "External Defacement": "外部篡改",
    "External Proxy": "外部代理",
    "External Remote Services": "外部远程服务",
    "Extra Window Memory Injection": "额外窗口内存注入",

    # F
    "Fallback Channels": "备用通道",
    "Fast Flux DNS": "快速通量 DNS",
    "File Deletion": "文件删除",
    "File and Directory Discovery": "文件和目录发现",
    "File and Directory Permissions Modification": "文件和目录权限修改",
    "File System Permissions Weakness": "文件系统权限弱点",
    "File Transfer Protocols": "文件传输协议",
    "File/Path Exclusions": "文件/路径排除",
    "Fileless Storage": "无文件存储",
    "Financial Theft": "金融盗窃",
    "Firmware Corruption": "固件损坏",
    "Forced Authentication": "强制认证",
    "Forge Web Credentials": "伪造 Web 凭据",

    # G
    "Gatekeeper Bypass": "Gatekeeper 绕过",
    "Gather Victim Host Information": "收集受害者主机信息",
    "Gather Victim Identity Information": "收集受害者身份信息",
    "Gather Victim Network Information": "收集受害者网络信息",
    "Gather Victim Org Information": "收集受害者组织信息",
    "Generate Content": "生成内容",
    "Golden Ticket": "黄金票据",
    "Group Policy Discovery": "组策略发现",
    "Group Policy Modification": "组策略修改",
    "Group Policy Preferences": "组策略首选项",
    "GUI Input Capture": "GUI 输入捕获",

    # H
    "Hardware": "硬件",
    "Hardware Additions": "硬件添加",
    "Hidden File System": "隐藏文件系统",
    "Hidden Files and Directories": "隐藏文件和目录",
    "Hidden Users": "隐藏用户",
    "Hidden Window": "隐藏窗口",
    "Hide Artifacts": "隐藏痕迹",
    "Hide Infrastructure": "隐藏基础设施",
    "HISTCONTROL": "HISTCONTROL历史控制",
    "Hijack Execution Flow": "劫持执行流",
    "Hooking": "钩子(Hooking)",
    "HTML Smuggling": "HTML 走私",
    "Hybrid Identity": "混合身份",
    "Hypervisor CLI": "虚拟机管理器 CLI",

    # I
    "IDE Extensions": "IDE 扩展",
    "IDE Tunneling": "IDE 隧道",
    "Identify Business Tempo": "识别业务节奏",
    "Identify Roles": "识别角色",
    "Ignore Process Interrupts": "忽略进程中断",
    "IIS Components": "IIS 组件",
    "Image File Execution Options Injection": "映像文件执行选项注入",
    "Impair Command History Logging": "破坏命令历史记录",
    "Impair Defenses": "破坏防御",
    "Impersonation": "冒充",
    "Implant Internal Image": "植入内部镜像",
    "Indicator Blocking": "指示器封锁",
    "Indicator Removal": "指示器清除",
    "Indicator Removal from Tools": "从工具清除指示器",
    "Indirect Command Execution": "间接命令执行",
    "Ingress Tool Transfer": "入口工具传输",
    "Inhibit System Recovery": "阻止系统恢复",
    "Input Capture": "输入捕获",
    "Input Injection": "输入注入",
    "Input Prompt": "输入提示",
    "Install Digital Certificate": "安装数字证书",
    "Install Root Certificate": "安装根证书",
    "Installer Packages": "安装程序包",
    "InstallUtil": "InstallUtil",
    "Inter-Process Communication": "进程间通信",
    "Internal Defacement": "内部篡改",
    "Internal Proxy": "内部代理",
    "Internal Spearphishing": "内部鱼叉钓鱼",
    "Internet Connection Discovery": "互联网连接发现",
    "Invalid Code Signature": "无效代码签名",
    "Invisible Unicode": "不可见 Unicode",
    "IP Addresses": "IP 地址",

    # J
    "JamPlus": "JamPlus构建工具",
    "JavaScript": "JavaScript",
    "Junk Code Insertion": "垃圾代码插入",
    "Junk Data": "垃圾数据",

    # K
    "Kerberoasting": "Kerberoasting攻击",
    "Kernel Modules and Extensions": "内核模块和扩展",
    "KernelCallbackTable": "内核回调表(KernelCallbackTable)",
    "Keychain": "钥匙串(Keychain)",
    "Keylogging": "键盘记录",

    # L
    "Lateral Tool Transfer": "横向工具传输",
    "Launch Agent": "启动代理(Launch Agent)",
    "Launch Daemon": "启动守护进程(Launch Daemon)",
    "Launchctl": "Launchctl服务管理",
    "LC_LOAD_DYLIB Addition": "LC_LOAD_DYLIB 添加",
    "Lifecycle-Triggered Deletion": "生命周期触发删除",
    "Link Target": "链接目标",
    "Linux and Mac Permissions": "Linux 和 Mac 权限",
    "ListPlanting": "列表植入(ListPlanting)",
    "LLMNR/NBT-NS Poisoning and Relay": "LLMNR/NBT-NS 投毒和中继",
    "LNK Icon Smuggling": "LNK 图标走私",
    "Local Account": "本地账户",
    "Local Accounts": "本地账户",
    "Local Data Staging": "本地数据暂存",
    "Local Email Collection": "本地邮件收集",
    "Local Groups": "本地组",
    "Local Job Scheduling": "本地作业调度",
    "Local Storage Discovery": "本地存储发现",
    "Log Enumeration": "日志枚举",
    "Login Hook": "登录 Hook",
    "Login Item": "登录项",
    "Login Items": "登录项",
    "Logon Script (Windows)": "登录脚本 (Windows)",
    "LSA Secrets": "LSA 密钥",
    "LSASS Driver": "LSASS 驱动",
    "LSASS Memory": "LSASS 内存",
    "Lua": "Lua",

    # M
    "Mail Protocols": "邮件协议",
    "Make and Impersonate Token": "创建并模拟令牌",
    "Malicious Copy and Paste": "恶意复制粘贴",
    "Malicious File": "恶意文件",
    "Malicious Image": "恶意图像",
    "Malicious Library": "恶意库",
    "Malicious Link": "恶意链接",
    "Malicious Shell Modification": "恶意Shell修改",
    "Malvertising": "恶意广告",
    "Malware": "恶意软件",
    "Mark-of-the-Web Bypass": "Web标记绕过(MOTW)",
    "Masquerade Account Name": "伪装账户名",
    "Masquerade File Type": "伪装文件类型",
    "Masquerade Task or Service": "伪装任务或服务",
    "Masquerading": "伪装",
    "Match Legitimate Resource Name or Location": "匹配合法资源名称或位置",
    "Mavinject": "Mavinject",
    "Messaging Applications": "消息应用程序",
    "MMC": "MMC",
    "Modify Authentication Process": "修改认证过程",
    "Modify Cloud Compute Configurations": "修改云计算配置",
    "Modify Cloud Compute Infrastructure": "修改云计算基础设施",
    "Modify Cloud Resource Hierarchy": "修改云资源层次结构",
    "Modify Existing Service": "修改现有服务",
    "Modify Registry": "修改注册表",
    "Modify System Image": "修改系统镜像",
    "Modify or Spoof Tool UI": "修改或伪造工具界面",
    "Mshta": "Mshta",
    "MSBuild": "MSBuild",
    "Msiexec": "Msiexec",
    "Multi-Factor Authentication": "多因素认证",
    "Multi-Factor Authentication Interception": "多因素认证拦截",
    "Multi-Factor Authentication Request Generation": "多因素认证请求生成",
    "Multi-Stage Channels": "多级通道",
    "Multi-hop Proxy": "多跳代理",
    "Multilayer Encryption": "多层加密",
    "Mutual Exclusion": "互斥",

    # N
    "Name Resolution Poisoning and SMB Relay": "名称解析投毒与SMB中继",
    "Native API": "原生 API",
    "Network Address Translation Traversal": "网络地址转换穿透",
    "Network Boundary Bridging": "网络边界桥接",
    "Network Denial of Service": "网络拒绝服务",
    "Network Device Authentication": "网络设备认证",
    "Network Device CLI": "网络设备 CLI",
    "Network Device Configuration Dump": "网络设备配置导出",
    "Network Device Firewall": "网络设备防火墙",
    "Network Devices": "网络设备",
    "Network Logon Script": "网络登录脚本",
    "Network Provider DLL": "网络提供者 DLL",
    "Network Security Appliances": "网络安全设备",
    "Network Service Discovery": "网络服务发现",
    "Network Share Connection Removal": "网络共享连接移除",
    "Network Share Discovery": "网络共享发现",
    "Network Sniffing": "网络嗅探",
    "Network Topology": "网络拓扑",
    "Network Trust Dependencies": "网络信任依赖",
    "New Service": "新建服务",
    "Non-Application Layer Protocol": "非应用层协议",
    "Non-Standard Encoding": "非标准编码",
    "Non-Standard Port": "非标准端口",
    "NTDS": "NTDS",
    "NTFS File Attributes": "NTFS 文件属性",

    # O
    "Obfuscated Files or Information": "混淆文件或信息",
    "Obtain Capabilities": "获取能力",
    "Odbcconf": "Odbcconf",
    "Office Application Startup": "Office 应用程序启动",
    "Office Template Macros": "Office 模板宏",
    "Office Test": "Office测试",
    "One-Way Communication": "单向通信",
    "OS Credential Dumping": "操作系统凭据转储",
    "OS Exhaustion Flood": "操作系统耗尽洪泛",
    "Outlook Forms": "Outlook 表单",
    "Outlook Home Page": "Outlook 主页",
    "Outlook Rules": "Outlook 规则",
    "Overwrite Process Arguments": "覆盖进程参数",

    # P
    "Parent PID Spoofing": "父进程 PID 伪造",
    "Pass the Hash": "哈希传递",
    "Pass the Ticket": "票据传递",
    "Password Cracking": "密码破解",
    "Password Filter DLL": "密码过滤器 DLL",
    "Password Guessing": "密码猜测",
    "Password Managers": "密码管理器",
    "Password Policy Discovery": "密码策略发现",
    "Password Spraying": "密码喷洒",
    "Patch System Image": "修补系统镜像",
    "Path Interception by PATH Environment Variable": "通过 PATH 环境变量路径劫持",
    "Path Interception by Search Order Hijacking": "通过搜索顺序劫持路径劫持",
    "Path Interception by Unquoted Path": "通过未引用路径劫持",
    "Peripheral Device Discovery": "外设发现",
    "Permission Groups Discovery": "权限组发现",
    "Phishing": "钓鱼",
    "Phishing for Information": "钓鱼获取信息",
    "Plist File Modification": "Plist 文件修改",
    "Plist Modification": "Plist 修改",
    "Pluggable Authentication Modules": "可插拔认证模块(PAM)",
    "Poisoned Pipeline Execution": "投毒流水线执行",
    "Polymorphic Code": "多态代码",
    "Port Knocking": "端口敲门",
    "Port Monitors": "端口监视器",
    "Portable Executable Injection": "可移植可执行文件(PE)注入",
    "Power Settings": "电源设置",
    "PowerShell": "PowerShell",
    "PowerShell Profile": "PowerShell 配置文件",
    "Pre-OS Boot": "操作系统启动前",
    "Prevent Command History Logging": "阻止命令历史记录",
    "Print Processors": "打印处理器",
    "Private Keys": "私钥",
    "Proc Memory": "Proc 内存",
    "Proc Filesystem": "Proc 文件系统",
    "Process Argument Spoofing": "进程参数伪造",
    "Process Discovery": "进程发现",
    "Process Doppelgänging": "进程分身(Doppelgänging)",
    "Process Hollowing": "进程镂空(Hollowing)",
    "Process Injection": "进程注入",
    "Protocol Tunneling": "协议隧道",
    "Protocol or Service Impersonation": "协议或服务模拟",
    "Proxy": "代理",
    "Ptrace System Calls": "Ptrace 系统调用",
    "PubPrn": "PubPrn",
    "Publish/Subscribe Protocols": "发布/订阅协议",
    "Purchase Technical Data": "购买技术数据",
    "Python": "Python",
    "Python Startup Hooks": "Python 启动钩子",

    # Q
    "Query Public AI Services": "查询公共 AI 服务",
    "Query Registry": "查询注册表",

    # R
    "Rc.common": "rc.common启动脚本",
    "RC Scripts": "RC 脚本",
    "RDP Hijacking": "RDP 劫持",
    "Re-opened Applications": "重新打开的应用程序",
    "Reduce Key Space": "缩减密钥空间",
    "Reflection Amplification": "反射放大",
    "Reflective Code Loading": "反射代码加载",
    "Registry Run Keys / Startup Folder": "注册表运行键 / 启动文件夹",
    "Regsvcs/Regasm": "Regsvcs/Regasm",
    "Regsvr32": "Regsvr32",
    "Relocate Malware": "重定位恶意软件",
    "Remote Access Hardware": "远程访问硬件",
    "Remote Access Tools": "远程访问工具",
    "Remote Data Staging": "远程数据暂存",
    "Remote Desktop Protocol": "远程桌面协议(RDP)",
    "Remote Desktop Software": "远程桌面软件",
    "Remote Email Collection": "远程邮件收集",
    "Remote Service Session Hijacking": "远程服务会话劫持",
    "Remote Services": "远程服务",
    "Remote System Discovery": "远程系统发现",
    "Rename Legitimate Utilities": "重命名合法工具",
    "Replication Through Removable Media": "通过可移动介质复制",
    "Resource Forking": "资源分支",
    "Resource Hijacking": "资源劫持",
    "Revert Cloud Instance": "恢复云实例",
    "Reversible Encryption": "可逆加密",
    "Right-to-Left Override": "从右到左覆盖(RTLO)",
    "Rogue Domain Controller": "恶意域控制器",
    "ROMMONkit": "ROMMONkit固件工具包",
    "Rootkit": "Rootkit",
    "Run Virtual Instance": "运行虚拟实例",
    "Rundll32": "Rundll32",
    "Runtime Data Manipulation": "运行时数据操纵",

    # S
    "Safe Mode Boot": "安全模式启动",
    "SAML Tokens": "SAML 令牌",
    "Scan Databases": "扫描数据库",
    "Scanning IP Blocks": "扫描 IP 块",
    "Scheduled Task": "计划任务",
    "Scheduled Task/Job": "计划任务/作业",
    "Scheduled Transfer": "计划传输",
    "Screen Capture": "屏幕捕获",
    "Screensaver": "屏幕保护程序",
    "Search Closed Sources": "搜索封闭来源",
    "Search Engines": "搜索引擎",
    "Search Open Technical Databases": "搜索公开技术数据库",
    "Search Open Websites/Domains": "搜索公开网站/域名",
    "Search Threat Vendor Data": "搜索威胁供应商数据",
    "Search Victim-Owned Websites": "搜索受害者自有网站",
    "Security Account Manager": "安全账户管理器(SAM)",
    "Security Software Discovery": "安全软件发现",
    "Security Support Provider": "安全支持提供者(SSP)",
    "Securityd Memory": "Securityd 内存",
    "Selective Exclusion": "选择性排除",
    "SEO Poisoning": "SEO 投毒",
    "Server": "服务器",
    "Server Software Component": "服务器软件组件",
    "Serverless": "无服务器(Serverless)",
    "Serverless Execution": "无服务器执行",
    "Service Exhaustion Flood": "服务耗尽洪泛",
    "Service Execution": "服务执行",
    "Service Registry Permissions Weakness": "服务注册表权限弱点",
    "Service Stop": "服务停止",
    "Services File Permissions Weakness": "服务文件权限弱点",
    "Services Registry Permissions Weakness": "服务注册表权限弱点",
    "Setuid and Setgid": "Setuid 和 Setgid",
    "Shared Modules": "共享模块",
    "Sharepoint": "SharePoint",
    "Shell History": "Shell 历史",
    "Shortcut Modification": "快捷方式修改",
    "SID-History Injection": "SID-History 注入",
    "Silver Ticket": "白银票据",
    "SIP and Trust Provider Hijacking": "SIP 和信任提供者劫持",
    "SMB/Windows Admin Shares": "SMB/Windows 管理共享",
    "SMS Pumping": "SMS 轰炸",
    "SNMP (MIB Dump)": "SNMP (MIB 导出)",
    "Social Engineering": "社会工程学",
    "Social Media": "社交媒体",
    "Social Media Accounts": "社交媒体账户",
    "Socket Filters": "Socket 过滤器",
    "Software": "软件",
    "Software Deployment Tools": "软件部署工具",
    "Software Discovery": "软件发现",
    "Software Extensions": "软件扩展",
    "Software Packing": "软件加壳",
    "Space after Filename": "文件名后空格",
    "Spearphishing Attachment": "鱼叉钓鱼附件",
    "Spearphishing Link": "鱼叉钓鱼链接",
    "Spearphishing Service": "鱼叉钓鱼服务",
    "Spearphishing via Service": "通过服务鱼叉钓鱼",
    "Spearphishing Voice": "语音鱼叉钓鱼",
    "Spoof Security Alerting": "伪造安全告警",
    "SQL Stored Procedures": "SQL 存储过程",
    "SSH": "SSH",
    "SSH Authorized Keys": "SSH 授权密钥",
    "SSH Hijacking": "SSH 劫持",
    "Stage Capabilities": "部署能力",
    "Standard Cryptographic Protocol": "标准加密协议",
    "Standard Encoding": "标准编码",
    "Startup Items": "启动项",
    "Steal Application Access Token": "窃取应用程序访问令牌",
    "Steal Web Session Cookie": "窃取 Web 会话 Cookie",
    "Steal or Forge Authentication Certificates": "窃取或伪造认证证书",
    "Steal or Forge Kerberos Tickets": "窃取或伪造 Kerberos 票据",
    "Steganography": "隐写术",
    "Stored Data Manipulation": "存储数据操纵",
    "Stripped Payloads": "剥离载荷",
    "Subvert Trust Controls": "颠覆信任控制",
    "Sudo": "Sudo",
    "Sudo and Sudo Caching": "Sudo 和 Sudo 缓存",
    "Sudo Caching": "Sudo 缓存",
    "Supply Chain Compromise": "供应链入侵",
    "SVG Smuggling": "SVG 走私",
    "Symmetric Cryptography": "对称加密",
    "SyncAppvPublishingServer": "SyncAppv发布服务器",
    "System Binary Proxy Execution": "系统二进制代理执行",
    "System Checks": "系统检查",
    "System Firmware": "系统固件",
    "System Information Discovery": "系统信息发现",
    "System Language Discovery": "系统语言发现",
    "System Location Discovery": "系统位置发现",
    "System Network Configuration Discovery": "系统网络配置发现",
    "System Network Connections Discovery": "系统网络连接发现",
    "System Owner/User Discovery": "系统所有者/用户发现",
    "System Script Proxy Execution": "系统脚本代理执行",
    "System Service Discovery": "系统服务发现",
    "System Services": "系统服务",
    "System Shutdown/Reboot": "系统关闭/重启",
    "System Time Discovery": "系统时间发现",
    "Systemctl": "Systemctl服务管理",
    "Systemd Service": "Systemd 服务",
    "Systemd Timers": "Systemd 定时器",

    # T
    "Taint Shared Content": "污染共享内容",
    "TCC Manipulation": "TCC 操纵",
    "Template Injection": "模板注入",
    "Temporary Elevated Cloud Access": "临时提升云访问权限",
    "Terminal Services DLL": "终端服务 DLL",
    "TFTP Boot": "TFTP 启动",
    "Thread Execution Hijacking": "线程执行劫持",
    "Thread Local Storage": "线程本地存储(TLS)",
    "Threat Intel Vendors": "威胁情报供应商",
    "Time Based Checks": "基于时间的检查",
    "Time Providers": "时间提供者",
    "Timestomp": "时间戳伪造(Timestomp)",
    "Token Impersonation/Theft": "令牌模拟/窃取",
    "Tool": "工具",
    "Traffic Duplication": "流量复制",
    "Traffic Signaling": "流量信号",
    "Transfer Data to Cloud Account": "传输数据到云账户",
    "Transmitted Data Manipulation": "传输数据操纵",
    "Transport Agent": "传输代理",
    "Trap": "Trap信号捕获",
    "Trust Modification": "信任修改",
    "Trusted Developer Utilities Proxy Execution": "可信开发工具代理执行",
    "Trusted Relationship": "信任关系",

    # U
    "Udev Rules": "Udev 规则",
    "Uncommonly Used Port": "非常用端口",
    "Unix Shell": "Unix Shell",
    "Unix Shell Configuration Modification": "Unix Shell 配置修改",
    "Unsecured Credentials": "未保护的凭据",
    "Unused/Unsupported Cloud Regions": "未使用/不支持的云区域",
    "Upload Malware": "上传恶意软件",
    "Upload Tool": "上传工具",
    "Use Alternate Authentication Material": "使用替代认证材料",
    "User Activity Based Checks": "基于用户活动的检查",
    "User Execution": "用户执行",

    # V
    "Valid Accounts": "有效账户",
    "VBA Stomping": "VBA 覆盖(Stomping)",
    "VDSO Hijacking": "VDSO 劫持",
    "Verclsid": "Verclsid",
    "Video Capture": "视频捕获",
    "Virtual Machine Discovery": "虚拟机发现",
    "Virtual Private Server": "虚拟专用服务器(VPS)",
    "Virtualization/Sandbox Evasion": "虚拟化/沙箱规避",
    "Visual Basic": "Visual Basic",
    "VNC": "VNC",
    "vSphere Installation Bundles": "vSphere 安装包",
    "Vulnerabilities": "漏洞",
    "Vulnerability Scanning": "漏洞扫描",

    # W
    "Web Cookies": "Web Cookie",
    "Web Portal Capture": "Web 门户捕获",
    "Web Protocols": "Web 协议",
    "Web Service": "Web 服务",
    "Web Services": "Web 服务",
    "Web Session Cookie": "Web 会话 Cookie",
    "Web Shell": "Web Shell",
    "Weaken Encryption": "削弱加密",
    "WHOIS": "WHOIS",
    "Wi-Fi Discovery": "Wi-Fi 发现",
    "Wi-Fi Networks": "Wi-Fi 网络",
    "Windows Admin Shares": "Windows 管理共享",
    "Windows Command Shell": "Windows 命令 Shell",
    "Windows Credential Manager": "Windows 凭据管理器",
    "Windows Host Firewall": "Windows 主机防火墙",
    "Windows Management Instrumentation": "Windows 管理规范(WMI)",
    "Windows Management Instrumentation Event Subscription": "WMI 事件订阅",
    "Windows Permissions": "Windows 权限",
    "Windows Remote Management": "Windows 远程管理(WinRM)",
    "Windows Service": "Windows 服务",
    "Winlogon Helper DLL": "Winlogon 辅助 DLL",
    "Wordlist Scanning": "字典扫描",
    "Written Content": "文字内容",

    # X
    "XDG Autostart Entries": "XDG 自启动条目",
    "XPC Services": "XPC 服务",
    "XSL Script Processing": "XSL 脚本处理",

    # Add-ins (special case)
    "Add-ins": "加载项(Add-ins)",
    "Active Setup": "Active Setup",
    "Application Exhaustion Flood": "应用程序耗尽洪泛",
    "AS-REP Roasting": "AS-REP Roasting",
    "Bootkit": "Bootkit",
    "CMSTP": "CMSTP",
    "ClickOnce": "ClickOnce",
    "Confluence": "Confluence",
    "COR_PROFILER": "COR_PROFILER探查器",
    "Credentials In Files": "文件中的凭据",
    "Cron": "Cron",
    "DCSync": "DCSync",
    "Disable Windows Event Logging": "禁用 Windows 事件日志记录",
    "Distributed Component Object Model": "分布式组件对象模型(DCOM)",
    "DNS": "DNS",
    "Email Addresses": "邮件地址",
    "Emond": "Emond事件监控守护进程",
    "Employee Names": "员工姓名",
    "Event Triggered Execution": "事件触发执行",
    "Firmware": "固件",
    "HISTCONTROL": "HISTCONTROL历史控制",
    "InstallUtil": "InstallUtil",
    "JamPlus": "JamPlus构建工具",
    "JavaScript": "JavaScript",
    "Kerberoasting": "Kerberoasting攻击",
    "KernelCallbackTable": "内核回调表(KernelCallbackTable)",
    "Launch Agent": "启动代理(Launch Agent)",
    "Launch Daemon": "启动守护进程(Launch Daemon)",
    "Launchctl": "Launchctl服务管理",
    "ListPlanting": "列表植入(ListPlanting)",
    "Lua": "Lua",
    "MMC": "MMC",
    "MSBuild": "MSBuild",
    "Mavinject": "Mavinject",
    "Mshta": "Mshta",
    "Msiexec": "Msiexec",
    "Netsh Helper DLL": "Netsh辅助DLL",
    "NTDS": "NTDS",
    "Odbcconf": "Odbcconf",
    "Office Test": "Office测试",
    "PowerShell": "PowerShell",
    "PubPrn": "PubPrn",
    "Python": "Python",
    "ROMMONkit": "ROMMONkit固件工具包",
    "Rc.common": "rc.common启动脚本",
    "Regsvcs/Regasm": "Regsvcs/Regasm",
    "Regsvr32": "Regsvr32",
    "Rootkit": "Rootkit",
    "Rundll32": "Rundll32",
    "SSH": "SSH",
    "Sudo": "Sudo",
    "SyncAppvPublishingServer": "SyncAppv发布服务器",
    "Systemctl": "Systemctl服务管理",
    "Trap": "Trap信号捕获",
    "Unix Shell": "Unix Shell",
    "VNC": "VNC",
    "Verclsid": "Verclsid",
    "Visual Basic": "Visual Basic",
    "WHOIS": "WHOIS",
    "Web Shell": "Web Shell",
}

# 缓解措施翻译
MITIGATION_TR = {
    "Active Directory Configuration Mitigation": "Active Directory 配置缓解",
    "Antivirus/Antimalware Mitigation": "防病毒/反恶意软件缓解",
    "Application Isolation and Sandboxing Mitigation": "应用程序隔离和沙箱缓解",
    "Audit Mitigation": "审计缓解",
    "Behavior Prevention on Endpoint Mitigation": "端点行为防护缓解",
    "Boot Integrity Mitigation": "启动完整性缓解",
    "Code Signing Mitigation": "代码签名缓解",
    "Credential Access Protection Mitigation": "凭证访问保护缓解",
    "Data Backup Mitigation": "数据备份缓解",
    "Data Loss Prevention Mitigation": "数据丢失防护缓解",
    "Do Not Mitigate": "不建议缓解",
    "Encrypt Sensitive Information Mitigation": "加密敏感信息缓解",
    "Environment Variable Permissions Mitigation": "环境变量权限缓解",
    "Execution Prevention Mitigation": "执行防护缓解",
    "Exploit Protection Mitigation": "漏洞利用防护缓解",
    "Filter Network Traffic Mitigation": "网络流量过滤缓解",
    "Limit Access to Resource Over Network Mitigation": "限制网络资源访问缓解",
    "Limit Hardware Installation Mitigation": "限制硬件安装缓解",
    "Limit Software Installation Mitigation": "限制软件安装缓解",
    "Multi-factor Authentication Mitigation": "多因素认证缓解",
    "Network Intrusion Prevention Mitigation": "网络入侵防护缓解",
    "Network Segmentation Mitigation": "网络分段缓解",
    "Operating System Configuration Mitigation": "操作系统配置缓解",
    "Password Policies Mitigation": "密码策略缓解",
    "Pre-compromise Mitigation": "入侵前缓解",
    "Privileged Account Management Mitigation": "特权账户管理缓解",
    "Privilege Separation": "权限分离",
    "Privileged Process Integrity Mitigation": "特权进程完整性缓解",
    "Remote Data Storage Mitigation": "远程数据存储缓解",
    "Restrict File and Directory Permissions Mitigation": "限制文件和目录权限缓解",
    "Restrict Library Loading Mitigation": "限制库加载缓解",
    "Restrict Registry Permissions Mitigation": "限制注册表权限缓解",
    "Restrict Web-Based Content Mitigation": "限制基于Web的内容缓解",
    "Scheduled Task Mitigation (removed)": "计划任务缓解(已移除)",
    "Service Registration Permissions Mitigation": "服务注册权限缓解",
    "Software Configuration Mitigation": "软件配置缓解",
    "SSL/TLS Inspection Mitigation": "SSL/TLS 检查缓解",
    "Threat Intelligence Program Mitigation": "威胁情报计划缓解",
    "Update Software Mitigation": "更新软件缓解",
    "User Account Control Mitigation": "用户账户控制缓解",
    "User Account Management Mitigation": "用户账户管理缓解",
    "User Training Mitigation": "用户培训缓解",
    "Vulnerability Scanning Mitigation": "漏洞扫描缓解",
    "Password Filter DLL Mitigation": "密码过滤器 DLL 缓解",
}

# 平台翻译
PLATFORM_TR = {
    "Windows": "Windows",
    "macOS": "macOS",
    "Linux": "Linux",
    "PRE": "PRE",
    "Office Suite": "Office 套件",
    "Identity Provider": "身份提供商",
    "SaaS": "SaaS",
    "IaaS": "IaaS",
    "Network Devices": "网络设备",
    "Containers": "容器",
    "ESXi": "ESXi",
    "Google Workspace": "Google Workspace",
    "Azure AD": "Azure AD",
    "Office 365": "Office 365",
}

# 权限要求翻译
PERMISSION_TR = {
    "User": "用户",
    "Administrator": "管理员",
    "root": "root",
    "SYSTEM": "SYSTEM",
}

# 加载中文描述翻译（如果文件存在）
import os as _os
DESC_ZH = {}
_desc_zh_path = _os.path.join(_os.path.dirname(__file__), 'desc_zh.json')
if _os.path.exists(_desc_zh_path):
    with open(_desc_zh_path, 'r', encoding='utf-8') as _f:
        DESC_ZH = json.load(_f)

def translate_technique(name):
    """翻译技术名称，优先使用词典，否则保留原名"""
    return TECHNIQUE_TR.get(name, name)

def translate_tactic(name):
    return TACTIC_TR.get(name, name)

def translate_tactic_desc(name):
    return TACTIC_DESC_TR.get(name, "")

def translate_mitigation(name):
    return MITIGATION_TR.get(name, name)

def translate_platform(p):
    return PLATFORM_TR.get(p, p)

def translate_permission(p):
    return PERMISSION_TR.get(p, p)


def process_stix(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        bundle = json.load(f)

    objects = bundle['objects']

    # 建立 ID -> object 索引
    by_id = {}
    for obj in objects:
        by_id[obj['id']] = obj

    # --- 提取战术 ---
    tactics = []
    matrix_order = []
    for obj in objects:
        if obj.get('type') == 'x-mitre-matrix' and not obj.get('x_mitre_deprecated'):
            matrix_order = obj.get('tactic_refs', [])
            break

    tactics_by_id = {}
    for obj in objects:
        if obj.get('type') == 'x-mitre-tactic' and not obj.get('x_mitre_deprecated'):
            ext_refs = obj.get('external_references', [])
            ext_id = ""
            for er in ext_refs:
                if er.get('source_name') == 'mitre-attack':
                    ext_id = er.get('external_id', '')
            tac_desc_cn = DESC_ZH.get(ext_id, translate_tactic_desc(obj['name']))
            tactics_by_id[obj['id']] = {
                'id': obj['id'],
                'external_id': ext_id,
                'name': obj['name'],
                'name_cn': translate_tactic(obj['name']),
                'shortname': obj.get('x_mitre_shortname', ''),
                'description': obj.get('description', ''),
                'description_cn': tac_desc_cn,
            }

    # 按 matrix 定义的顺序排列战术
    for tid in matrix_order:
        if tid in tactics_by_id:
            tactics.append(tactics_by_id[tid])

    # --- 提取技术 (attack-patterns) ---
    techniques = {}
    for obj in objects:
        if obj.get('type') == 'attack-pattern' and not obj.get('x_mitre_deprecated'):
            ext_refs = obj.get('external_references', [])
            ext_id = ""
            url = ""
            for er in ext_refs:
                if er.get('source_name') == 'mitre-attack':
                    ext_id = er.get('external_id', '')
                    url = er.get('url', '')
            platforms = [translate_platform(p) for p in obj.get('x_mitre_platforms', [])]
            permissions = [translate_permission(p) for p in obj.get('x_mitre_permissions_required', [])]

            desc_cn = DESC_ZH.get(ext_id, '')
            desc_en = obj.get('description', '')
            techniques[obj['id']] = {
                'id': obj['id'],
                'external_id': ext_id,
                'name': obj['name'],
                'name_cn': translate_technique(obj['name']),
                'description': desc_en,
                'description_cn': desc_cn,
                'platforms': platforms,
                'permissions': permissions,
                'url': url,
                'is_subtechnique': '.' in ext_id,
                'parent_id': ext_id.split('.')[0] if '.' in ext_id else None,
            }

    # --- 提取组 (intrusion-sets) ---
    groups = {}
    for obj in objects:
        if obj.get('type') == 'intrusion-set' and not obj.get('x_mitre_deprecated'):
            ext_refs = obj.get('external_references', [])
            ext_id = ""
            for er in ext_refs:
                if er.get('source_name') == 'mitre-attack':
                    ext_id = er.get('external_id', '')
            aliases = obj.get('aliases', [])
            grp_desc_cn = DESC_ZH.get(ext_id, '')
            groups[obj['id']] = {
                'id': obj['id'],
                'external_id': ext_id,
                'name': obj['name'],
                'aliases': aliases,
                'description': obj.get('description', ''),
                'description_cn': grp_desc_cn,
            }

    # --- 提取恶意软件 ---
    malware = {}
    for obj in objects:
        if obj.get('type') == 'malware' and not obj.get('x_mitre_deprecated'):
            ext_refs = obj.get('external_references', [])
            ext_id = ""
            for er in ext_refs:
                if er.get('source_name') == 'mitre-attack':
                    ext_id = er.get('external_id', '')
            mal_desc_cn = DESC_ZH.get(ext_id, '')
            malware[obj['id']] = {
                'id': obj['id'],
                'external_id': ext_id,
                'name': obj['name'],
                'description': obj.get('description', ''),
                'description_cn': mal_desc_cn,
                'platforms': [translate_platform(p) for p in obj.get('x_mitre_platforms', [])],
            }

    # --- 提取工具 ---
    tools = {}
    for obj in objects:
        if obj.get('type') == 'tool' and not obj.get('x_mitre_deprecated'):
            ext_refs = obj.get('external_references', [])
            ext_id = ""
            for er in ext_refs:
                if er.get('source_name') == 'mitre-attack':
                    ext_id = er.get('external_id', '')
            tool_desc_cn = DESC_ZH.get(ext_id, '')
            tools[obj['id']] = {
                'id': obj['id'],
                'external_id': ext_id,
                'name': obj['name'],
                'description': obj.get('description', ''),
                'description_cn': tool_desc_cn,
                'platforms': [translate_platform(p) for p in obj.get('x_mitre_platforms', [])],
            }

    # --- 提取缓解措施 ---
    mitigations = {}
    for obj in objects:
        if obj.get('type') == 'course-of-action' and not obj.get('x_mitre_deprecated'):
            ext_refs = obj.get('external_references', [])
            ext_id = ""
            for er in ext_refs:
                if er.get('source_name') == 'mitre-attack':
                    ext_id = er.get('external_id', '')
            mit_desc_cn = DESC_ZH.get(ext_id, '')
            mitigations[obj['id']] = {
                'id': obj['id'],
                'external_id': ext_id,
                'name': obj['name'],
                'name_cn': translate_mitigation(obj['name']),
                'description': obj.get('description', ''),
                'description_cn': mit_desc_cn,
            }

    # --- 使用 kill_chain_phases 建立技术 -> 战术映射 ---
    # 先建立 shortname -> tactic_id 的索引
    shortname_to_tactic = {}
    for tid, t in tactics_by_id.items():
        shortname_to_tactic[t['shortname']] = tid

    tech_to_tactics = {}  # tech_id -> [tactic_ids]
    for tid, tech in techniques.items():
        # 从原始 STIX 对象获取 kill_chain_phases
        stix_obj = by_id.get(tid, {})
        kc_phases = stix_obj.get('kill_chain_phases', [])
        for kc in kc_phases:
            if kc.get('kill_chain_name') == 'mitre-attack':
                phase_name = kc.get('phase_name', '')
                if phase_name in shortname_to_tactic:
                    tactic_id = shortname_to_tactic[phase_name]
                    if tid not in tech_to_tactics:
                        tech_to_tactics[tid] = []
                    if tactic_id not in tech_to_tactics[tid]:
                        tech_to_tactics[tid].append(tactic_id)

    # --- 提取关系 ---
    # 子技术 -> 父技术 (subtechnique-of)
    sub_of = {}  # child_tech_id -> parent_tech_id
    # 技术 -> 组 (group uses technique)
    tech_to_groups = {}  # tech_id -> [group_ids]
    group_to_techs = {}  # group_id -> [tech_ids]
    # 技术 -> 恶意软件/工具 (software uses technique)
    tech_to_software = {}  # tech_id -> [sw_ids]
    # 技术 -> 缓解措施
    tech_to_mitigations = {}  # tech_id -> [mitigation_ids]

    for obj in objects:
        if obj.get('type') != 'relationship':
            continue
        if obj.get('x_mitre_deprecated', False):
            continue
        rel_type = obj.get('relationship_type', '')
        source = obj.get('source_ref', '')
        target = obj.get('target_ref', '')

        # 子技术关系
        if rel_type == 'subtechnique-of' and source in techniques and target in techniques:
            sub_of[source] = target

        # 组使用技术 (intrusion-set uses attack-pattern)
        elif rel_type == 'uses' and source in groups and target in techniques:
            if target not in tech_to_groups:
                tech_to_groups[target] = []
            if source not in tech_to_groups[target]:
                tech_to_groups[target].append(source)
            if source not in group_to_techs:
                group_to_techs[source] = []
            if target not in group_to_techs[source]:
                group_to_techs[source].append(target)

        # 恶意软件/工具使用技术
        elif rel_type == 'uses' and (source in malware or source in tools) and target in techniques:
            if target not in tech_to_software:
                tech_to_software[target] = []
            if source not in tech_to_software[target]:
                tech_to_software[target].append(source)

        # 缓解措施缓解技术 (course-of-action mitigates attack-pattern)
        elif rel_type == 'mitigates' and source in mitigations and target in techniques:
            if target not in tech_to_mitigations:
                tech_to_mitigations[target] = []
            if source not in tech_to_mitigations[target]:
                tech_to_mitigations[target].append(source)
    # --- 构建矩阵结构 ---
    # 为每个战术找到其技术列表（排除子技术）
    matrix = []
    for tactic in tactics:
        tactic_techs = []
        for tech_id, tactic_ids in tech_to_tactics.items():
            if tactic['id'] in tactic_ids and tech_id in techniques:
                tech = techniques[tech_id]
                if not tech['is_subtechnique']:
                    # 找到该技术的子技术
                    sub_ids = []
                    for child_id, parent_id in sub_of.items():
                        if parent_id == tech_id and child_id in techniques:
                            sub_ids.append(child_id)
                    # 按 ID 排序子技术
                    sub_ids.sort(key=lambda x: techniques[x]['external_id'])
                    tech_copy = dict(tech)
                    tech_copy['subtechniques'] = [techniques[sid] for sid in sub_ids]
                    tactic_techs.append(tech_copy)

        # 按 external_id 排序技术
        tactic_techs.sort(key=lambda x: x['external_id'])
        matrix.append({
            'tactic': tactic,
            'techniques': tactic_techs,
        })

    # --- 输出 ---
    output = {
        'matrix': matrix,
        'tactics': tactics,
        'techniques': {k: v for k, v in techniques.items() if not v['is_subtechnique']},
        'subtechniques': {k: v for k, v in techniques.items() if v['is_subtechnique']},
        'all_techniques': techniques,
        'groups': groups,
        'malware': malware,
        'tools': tools,
        'mitigations': mitigations,
        'group_to_techs': group_to_techs,
        'tech_to_groups': tech_to_groups,
        'tech_to_software': tech_to_software,
        'tech_to_mitigations': tech_to_mitigations,
        'tech_to_tactics': tech_to_tactics,
    }

    # 写出为 JS 文件 (window.ATTACK_DATA = ...)
    json_str = json.dumps(output, ensure_ascii=False, indent=2)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(f"// MITRE ATT&CK 中文本地化数据\n// 自动生成，请勿手动编辑\nwindow.ATTACK_DATA = {json_str};\n")

    print(f"输出: {output_path}")
    print(f"战术: {len(tactics)}")
    tech_count = len([t for t in techniques.values() if not t['is_subtechnique']])
    sub_count = len([t for t in techniques.values() if t['is_subtechnique']])
    print(f"技术: {tech_count} 个父技术 + {sub_count} 个子技术 = {len(techniques)}")
    print(f"组: {len(groups)}")
    print(f"恶意软件: {len(malware)}")
    print(f"工具: {len(tools)}")
    print(f"缓解措施: {len(mitigations)}")

    # 检查未翻译的技术名
    missing = []
    for t in techniques.values():
        if t['name_cn'] == t['name']:
            missing.append(t['name'])
    if missing:
        print(f"\n未翻译的技术名 ({len(missing)}):")
        for m in sorted(missing):
            print(f"  {m}")


if __name__ == '__main__':
    process_stix('enterprise-attack.json', 'data.js')
