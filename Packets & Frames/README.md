
**Packets** and **frames** are small pieces of data that, when forming together, make a larger piece of information or message. However, they are two different things in the OSI model.


1. A **`frame`** is at layer 2 - the data link layer, meaning there is **_no such information as IP addresses_**.

hink of this as putting an envelope within an envelope and sending it away. The first envelope will be the packet that you mail, but once it is opened, the envelope within still exists and contains data (this is a frame).

This process is called encapsulation which we discussed in room 3: the OSI model. At this stage, it's safe to assume that when we are talking about anything IP addresses, we are talking about packets. When the encapsulating information is stripped away, we're talking about the frame itself.


2. **Packets** are an efficient way of communicating data across networked devices such as those explained in Task 1. Because this data is exchanged in small pieces, there is less chance of bottlenecking occurring across a network than large messages being sent at once.

<ins>Question</ins>


1. What is the name for a piece of data when it does have IP addressing information?

--> packet

2. What is the name for a piece of data when it does not have IP addressing information?

--> frame

