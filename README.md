# Documentation

## Bot interactions with network

### [DONE] - ```!ping google.fr 3```
```

timestamp: 2020-04-13 23:51:33
destination: google.fr
packet_transmit: 3
packet_receive: 3
packet_loss_count: 0
packet_loss_rate: 0.0
rtt_min: 37.217
rtt_avg: 40.25
rtt_max: 43.23
rtt_mdev: 2.466
packet_duplicate_count: 0
packet_duplicate_rate: 0.0

```
* replace ping with tcpping or hping3 ? 
    * https://github.com/deajan/tcpping/blob/master/tcpping
    * http://www.hping.org/ hping3

### [DONE] - ```!reach google.fr```
```
timestamp: 2020-04-13 23:54:20.396937
url-target: https://google.fr
http-return-code: 200
namelookup-time: 0.185807
connect-time: 0.269494
Time-To-First-Byte: 0.565642
total-time: 0.690115
redirect-count: 1
cert-health-(1=KO): 0
```

### [DONE] - ```!mbox or !mailbox``` AND ```!mbox clearall or !mailbox clearall```
```
!mbox
2020-04-12 11:15:43+02:00: ${subject}
!!! : 1 mail have been found in the mailbox !!!
```
```
!mailbox clearall
mailbox ${MAILBOXNAME} (${FOLDER_SELECTED}) has been cleared !
```
```
!mbox
:):):) 0 mails in the mailbox in the last 24h ${MAILBOXNAME} (${FOLDER_SELECTED})
```

### TODO - ```!scan IP.IP.IP.IP 22,80,443```

It should give you clear overview if port is filtered with firewall,not routed or closed. 
Nmap binary shoud be fine with a lot of options

## Bot interactions with compute

### [DONE] - ```!uh or !uhash or !user_hash" or !userhash```
``` $6$rounds=656000$x7XatslsbOoLxesw$ZV3Ju24qp47JEsubyB7CJ8eI2l8mE3L1DSee345lrdZ2doVZunXXhkw3kISrLk9vEvU2mXuL5SHyrbOnvUoGT1 ### .|\Wr|.ImO{$+6/5 ```

Return Linux standard hash password and after ### the clear password associated

### [DONE] - ```!mh or !mhash or !mysql_hash" or !mysqlhash```
``` $5$rounds=535000$XP.V8wNQ3ium8AC8$sDXC4ib5RNTuTi/Or55kYaxxRm1pRCbhw/da435A.v4 ### ;A4EigyiqcpZ^DZ& ```

Return mysql 8.X hash password and after ### the clear password associated



# ROADMAP
    * Feedback on redmines tickets where we want global communication:
        * A tag on redmine could be catched by the bot and publicly annonce in #important channels the ticket title and body
    * Zabbix monitoring alerts list with default filtering
    * Get all tickets created with default filters from redmine
    * Guided help/startup toolkit for new people who are new in my team / my company
    * Coding Kamoulox projects
    * BonjourMadame posts
    * Famous punchline from famous actors ( C*** N*** , JCV , From our team .. etc )
    * custom responses when errors occurs

# Thanks to [nio-template project](https://github.com/anoadragon453/nio-template) !

Easy starter kit to anybody want to begin automation of dumb and boring tasks !

This template is also based on [matrix-nio](https://github.com/poljar/matrix-nio). 
