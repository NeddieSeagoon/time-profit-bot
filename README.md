# time-profit-bot
A discord bot to calculate profit vs time

Planned v0.1 features:
- quick-to-type command like `.pt`
- one optional argument: -r, for round trip
- one mission type: simple
  - either `start -> complete objective` OR if roundtrip `start -> complete obj. -> finish`
- takes wallet input before mission and at end

usage conversation example:
```
user: .pt -r
bot: please enter wallet amount
user: 100000
bot: okay please enter '.' to start timer
user: .
bot: timer started. enter '.' when mission objective completed.
user: .
bot: mission objective time recorded. enter '.' when finished mission.
user: .
bot: timer stopped. enter new wallet amount
user: 120000
bot: your time was <duration> and profit <profit>. Your profit per minute was <profit_per_minute>.
```
