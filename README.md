# PynamicDNS
Python script to perform dynamic DNS using AWS Route53 on a Raspberry Pi or other Linux hosts

See [this post at tynick.com](https://tynick.com/blog/03-16-2020/pynamicdns-dynamic-dns-with-raspberry-pi-python-and-aws/ "tynick.com PynamicDNS Instructions") for full instructions.

## Run Manually

You can run the script manually to test.

It will look something like the following if your public IP doesn't match your DNS record...

```
root@raspberrypi:~# python3 ~/PynamicDNS/PynamicDNS.py pynamicdns.tynick.com X0XXXXXX000X0
---------------------------
Public IP:             xx.xx.xx.xx
pynamicdns.tynick.com: yy.yy.yy.yy
---------------------------
DNS VALUE DOES NOT MATCH PUBLIC IP
DNS CHANGE SUCCESSFUL
root@raspberrypi:~#
```

It will look something like the following if your public IP matches your DNS record...

```
root@raspberrypi:~# python3 ~/PynamicDNS/PynamicDNS.py pynamicdns.tynick.com X0XXXXXX000X0
---------------------------
Public IP:             xx.xx.xx.xx
pynamicdns.tynick.com: xx.xx.xx.xx
---------------------------
NO CHANGE NEEDED
root@raspberrypi:~#
```

## Run Via Cron

Once you confirm that it is working, you'll want to make a new cronjob so that it checks your IP every 5 minutes.

```
*/5 * * * * python3 ~/PynamicDNS/PynamicDNS.py pynamicdns.tynick.com X0XXXXXX000X0
```
