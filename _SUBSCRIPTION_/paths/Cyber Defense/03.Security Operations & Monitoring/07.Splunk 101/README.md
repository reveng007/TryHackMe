Task1: Intro to Splunk
----

Typically when people think of a SIEM, they think of Splunk, and rightly so. Per the Splunk website, they boast that 91 of the Fortune 100 use Splunk. 

Splunk is not only used for security; it's used for data analysis, DevOps, etc. But before speaking more on Splunk, what is a SIEM exactly?

A **SIEM (Security Information and Event Management)** is a software solution that provides a central location to collect log data from multiple sources within your environment. This data is aggregated and normalized, which can then be queried by an analyst.

As stated by [Varonis](https://www.varonis.com/blog/what-is-siem/), there are 3 critical capabilities for a SIEM:

- Threat detection
- Investigation
- Time to respond


Some other SIEM features:

- Basic security monitoring
- Advanced threat detection
- Forensics & incident response
- Log collection
- Normalization
- Notifications and alerts
- Security incident detection
- Threat response workflow


This room is a general overview of Splunk and its core features. Having experience with Splunk will help your resume stick out from the rest.

Splunk was named a "Leader" in [Gartner's](https://www.splunk.com/en_us/form/gartner-siem-magic-quadrant.html) 2020 Magic Quadrant for Security Information and Event Management.

Per Gartner, "Thousands of organizations around the world use Splunk as their SIEM for security monitoring, advanced threat detection, incident investigation and forensics, incident response, SOC automation and a wide range of security analytics and operations use cases."


Downloaded Splunk Enterprise at /opt/splunk:

To start:
```
$ sudo ./opt/splunk/bin/splunk start
```

To Stop:
```
$ sudo ./opt/splunk/bin/splunk stop
```

To see status:
```
$ sudo ./opt/splunk/bin/splunk status
```

`To access: go to: http://127.0.0.1:8000`
```
USER: admin
PASS: password
```

Let's look at each section, or panel, that makes up the home screen. The top panel is the **Splunk Bar** (below image). 

![](splunk-bar.png?raw=true)

In the Splunk Bar, you can see system-level messages (**Messages**), configure the Splunk instance (**Settings**), review the progress of jobs (**Activity**), miscellaneous information such as tutorials (**Help**), and a search feature (**Find**). 

The ability to switch between installed Splunk apps instead of using the **Apps panel** can be achieved from the Splunk Bar, like in the image below.

![](splunk-bar2.png?raw=true)

Next is the **Apps Panel**.  In this panel, you can see the apps installed for the Splunk instance. 

The default app for every Splunk installation is **Search & Reporting**.

![](splunk-apps-panel.png?raw=true)


The next section is **Explore Splunk**. This panel contains quick links to add data to the Splunk instance, add new Splunk apps, and access the Splunk documentation. 

![](explore-splunk.png?raw=true)

The last section is the **Home Dashboard**. By default, no dashboards are displayed. You can choose from a range of dashboards readily available within your Splunk instance. You can select a dashboard from the dropdown menu or by visiting the **dashboards listing page**.

![](splunk-add-dashboard.gif?raw=true)


