1. Task1: Introduction
---

1. In a red team operation, you might start with no more than a company name, from which you need to start gathering information about the target. This is where reconnaissance comes into play.

2. Reconnaissance (recon) can be defined as a preliminary survey or observation of your target (client) without alerting them to your activities.

3. If your recon activities create too much noise, the other party would be alerted, which might decrease the likelihood of your success.

The tasks of this room cover the following topics:
```
1. Types of reconnaissance activities
2. WHOIS and DNS-based reconnaissance
3. Advanced searching
4. Searching by image
5. Google Hacking
6. Specialized search engines
7. Recon-ng
8. Maltego
```
Some specific objectives we'll cover include:
```
1. Discovering subdomains related to our target company
2. Gathering publicly available information about a host and IP addresses
3. Finding email addresses related to the target
4. Discovering login credentials and leaked passwords
6. Locating leaked documents and spreadsheets
```
2. Task2: Taxonomy of Reconnaissance:
-----

Reconnaissance can be broken down into two parts:

1. Passive reconnaissance
2. Active reconnaissance, as explained in Task 2.

In this room, we will be focusing on passive reconnaissance, i.e., techniques that don’t alert the target or create 'noise'. In later rooms, we will use active reconnaissance tools that tend to be noisy by nature.

***Passive recon*** doesn't require interacting with the target.
In other words, you aren't sending any packets or requests to the target or the systems your target owns.
Instead, passive recon relies on publicly available information that is collected and maintained by a third party.

Open Source Intelligence (OSINT) is used to collect information about the target and can be as simple as viewing a target's publicly available social media profile.
Example information that we might collect includes domain names, IP address blocks, email addresses, employee names, and job posts.

Visit [Passive Recon Room]

***Active recon*** requires interacting with the target by sending requests and packets and observing if and how it responds.

The responses collected - or lack of responses - would enable us to expand on the picture we started developing using passive recon.

Visit [Active Recon Room]

Some information that we would want to discover include live hosts, running servers, listening services, and version numbers.

***Active recon*** can be classified as:
	1. **External Recon**: Conducted outside the target's network and focuses on the externally facing assets assessable from the Internet. One example is running Nikto from outside the company network.

	2. **Internal Recon**: Conducted from within the target company's network. In other words, the pentester or red teamer might be physically located inside the company building. In this scenario, they might be using an exploited host on the target's network. An example would be using Nessus to scan the internal network using one of the target’s computers.

3. Task3: Built-in Tools:
----

This task focuses on:

- `whois`
- `dig`, `nslookup`, `host`
- `traceroute`/`tracert`

***whois***:
1. Whois, pronounced "who is", is a system that allows users to look up the name and contact information of a registered domain name (website).
2. When someone registers a new domain, the registrar(an official responsible for keeping a register or official records) asks for specific contact information, most of which is required by The Internet Corporation for Assigned Names and Numbers (ICANN).
3. This information is held in the Whois Database, which is available for anyone to access through ***a Whois lookup tool***.
4. All you need is a website address to search for and contact the party responsible for any given internet resource.

`whois` provides us with:

> Registrar: an official responsible for keeping a register or official records.

- Registrar WHOIS server
- Registrar URL
- Record creation date
- Record update date
- Registrant contact info and address (unless withheld for privacy)
- Admin contact info and address (unless withheld for privacy)
- Tech contact info and address (unless withheld for privacy)

```
$ whois github.com
```
It is possible to gain a lot of valuable information with only a domain name.
After a `whois lookup`, we might get lucky and find _names_, _email addresses_,_postal addresses_, and _phone numbers_, in addition to other technical information.
At the end of the whois query, we find `the authoritative name servers` for the domain in question.


