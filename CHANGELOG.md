# Changelog

## 0.5.0

- Display event title correctly for series event (fixes #77)
- Display location of event on complete NZ map (fixes #76)
- Add flat pages (fixes #75)
- Allow HTML in event session titles and descriptions, using TinyMCE (fixes #73)
- Add UC logo to homepage frontend (fixes #64)
- Align series image with text correctly

## 0.4.3

- Fix bug where ThirdPartyEvents cannot be created as they do not contain a series attribute ([fixes #62](https://github.com/uccser/cs4teachers/issues/62))
- Alter design of series cards to contain subtitle formatting ([fixes #61](https://github.com/uccser/cs4teachers/issues/61))
- Increase size of sponsor logos to be clearer

## 0.4.2

- Fix bug where series logo was prefixed with local media location ([fixes #58](https://github.com/uccser/cs4teachers/issues/58))
- Add and display series subtitle
- Format event resource count on schedule to stand out from description

## 0.4.1

- Fix bug where admin interface does not allow changing object containing image ([fixes #56](https://github.com/uccser/cs4teachers/issues/56))
- Fix name of EventImage to Event relationship ([fixes #55](https://github.com/uccser/cs4teachers/issues/55))
- Fix bug where sponsor logo was prefixed with local media location

## 0.4.0

- Allow event to be part of series ([fixes #44](https://github.com/uccser/cs4teachers/issues/44))
- Do not require sponsor for an event ([fixes #41](https://github.com/uccser/cs4teachers/issues/41))
- Allow media uploads for objects ([fixes #45](https://github.com/uccser/cs4teachers/issues/45))
- Add start and end date fields directly to event model ([fixes #52](https://github.com/uccser/cs4teachers/issues/52))
- Add warning to third party event page ([fixes #42](https://github.com/uccser/cs4teachers/issues/42))
- Show third party event description as full width ([fixes #40](https://github.com/uccser/cs4teachers/issues/40))
- Display resource count for each session on event page ([fixes #51](https://github.com/uccser/cs4teachers/issues/51))
- Open resources and sponsors in new tab ([fixes #48](https://github.com/uccser/cs4teachers/issues/48))
- Remove restriction of unique event names ([fixes #43](https://github.com/uccser/cs4teachers/issues/43))
- Add test suite and code coverage ([fixes #29](https://github.com/uccser/cs4teachers/issues/29))

## 0.3.1

- Fix third party event page bug ([fixes #37](https://github.com/uccser/cs4teachers/issues/37))
- Fix navbar layout on mobile devices ([fixes #38](https://github.com/uccser/cs4teachers/issues/38))
- Display third party URL link as button for consistency

## 0.3.0

- Fix typo on homepage
- Add favicon ([fixes #11](https://github.com/uccser/cs4teachers/issues/11))
- Display locations with Google Maps ([fixes #20](https://github.com/uccser/cs4teachers/issues/20))
- Add version number context processor and display version on website

## 0.2.0

- Update django from 1.11.2 to 1.11.3
- Fix bug where event has no primary location ([fixes #26](https://github.com/uccser/cs4teachers/issues/26))
- Fix bug in third party admin interface ([fixes #27](https://github.com/uccser/cs4teachers/issues/27))
- Add migration file for event slug changes
- Add location to event list page
- Fix template when multiple events are displayed
- Add continous testing by Travis CI (includes style checks) ([fixes #28](https://github.com/uccser/cs4teachers/issues/28))
- Add PyUP support

## 0.1.0

Initial release of website on Heroku.

Allows storing and viewing of:

- Official events
- Third party events
- Sessions
- Locations
- Resources
- Sponsors
