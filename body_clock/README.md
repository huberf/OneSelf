# QS Body Clock

The idea behind this is one can keep track of valuable metrics that occur
at set times or time ranges throughout the day to get an at a glance view of how
various aspects will impact your day. Visually the system will have a clock of the day and
around its edge various events are placed such as ones highest blood pressure,
sleep period, best time for exercise and other lifestyle and physiological
components.


## Setup
1. Run `npm install`
2. Execute `npm start`
3. Setup events in `events.json`

## Event Types
An instantaneous event such as the moment of lowest heart rate is described by:
```
{
  "name": "Lowest Heart Rate",
  "time": "03:43"
}
```

An event that occurs over an extended period of time:
```
{
  "name": "Sleep",
  "start": "21:30",
  "end": "05:00"
}
```

## Sources
Initial clock SVG from
[https://html5demos.com/svg-clock/](https://html5demos.com/svg-clock/)
