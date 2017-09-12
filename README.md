# drivingtest
I had a friend that was trying to pass their driving test but the test centers were booked up for months. It is possible to reschedule your test if a free slot becomes available but there is no notification system on the website to tell you when slots become available, you have to manually log in each time.

So I threw together the following script to check for available slots automatically and email when they become available.

This was run every 30 minutes in a cron job (any faster than that and it will trigger a captcha check).

It's very rough but I can't develop it further as they have passed so I no longer a set of valid account details to use on the website. Hopefully it might be useful to someone else in the future though.
