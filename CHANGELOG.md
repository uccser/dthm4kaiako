# Changelog

## 0.10.0

- Improve detection of resource component types:
    - Add PDF and spreadsheet types.
    - Detect type of Google Drive documents using Google Drive API.
    - Set YouTube and Vimeo as video components.
- Add the following classifiers for resources:
    - Language
    - Year level
    - Curriculum learning area
    - Technology curriculum strand
    - Progress outcome
    - NZQA standard
- Fix bug where a resource could be a component of itself.
- Fix bug where users with no username could not login into admin.
- Dependencies changes:
    - Add google-api-python-client 1.7.8.
    - Update flake8 from 3.7.5 to 3.7.6.
    - Update mypy from 0.660 to 0.670.
    - Update pytest from 4.2.0 to 4.3.0.

## 0.9.4

- Fix bug where DTTA news articles added after server start are not available. ([fixes #259](https://github.com/uccser/dthm4kaiako/issues/259))

## 0.9.3

- Fix bug where DTTA news articles are filtered by the wrong timezone.
- Fix bug where Resource 'component of' links do not link correctly. ([fixes #261](https://github.com/uccser/dthm4kaiako/issues/261))
- Fix date within FAQ question.
- Update dependencies:
    - Update flake8 from 3.7.4 to 3.7.5.
    - Update sphinx from 1.8.3 to 1.8.4.

## 0.9.2

- Fix bug where contact form doesn't send copy to sender.

## 0.9.1

- Fix bug where resource component types were not detected correctly. ([fixes #253](https://github.com/uccser/dthm4kaiako/issues/253))
- Add missing spacing element for resource list page.
- Fix issue in production secrets.

## 0.9.0

- Enable user registration.
- Improve visual design of resource hub. ([fixes #226](https://github.com/uccser/dthm4kaiako/issues/226))
- Improve detection of resource component types.
- Add source and audience tags to DTTA news articles. ([fixes #217](https://github.com/uccser/dthm4kaiako/issues/217))
- Add contact us page.
- Enable limited API for resources. ([fixes #249](https://github.com/uccser/dthm4kaiako/issues/249))

## 0.8.2

- Fix bug where resource URL component doesn't link correctly. ([fixes #221](https://github.com/uccser/dthm4kaiako/issues/221))
- Show readable URLs for DTTA pages and news articles.
- Fix typos.

## 0.8.1

- Add DTTA related links for DTTA homepage backend frontend. ([fixes #218](https://github.com/uccser/dthm4kaiako/issues/218))
- Update formatting of DTTA news article listings and articles.
- Correct path for resource media uploads.
- Add download link for uploaded resource files.

## 0.8.0

- Add basic resource hub. ([fixes #198](https://github.com/uccser/dthm4kaiako/issues/198))
- Separate static and file files to different Google Cloud Storage buckets.

## 0.7.0

- Add new look to website including logo and brand colours. ([fixes #191](https://github.com/uccser/dthm4kaiako/issues/191) [#192](https://github.com/uccser/dthm4kaiako/issues/192) [#193](https://github.com/uccser/dthm4kaiako/issues/193))
- Add about, FAQ, and contact us pages. ([fixes #200](https://github.com/uccser/dthm4kaiako/issues/200))
- Load third party static files from NPM. ([fixes #202](https://github.com/uccser/dthm4kaiako/issues/202))
- Fix bug where unpublished DTTA pages are shown. ([fixes #215](https://github.com/uccser/dthm4kaiako/issues/215))
- Add Google Analytics. ([fixes #205](https://github.com/uccser/dthm4kaiako/issues/205))

## 0.6.0

This release completely rewrites the project as a website for all NZ DTHM educators.
Adding a resource and community hub to the event website was planned in the initial design, however due to new DTHM curricula, a full redesign and rename was appropriate.

- Project based off `cookiecutter-django` and our Docker setup for Google Cloud Platform deployments.
- Uses Django 2.1 to set us up for easy adoption of Django 2.2 LTS when released in a few months.
- Framework setup for resource, event, and DTTA hubs.
- Includes basic pages for DTTA pages.

## 0.5.3

- Allow manual configuration of slug values. ([fixes #14](https://github.com/uccser/dthm4kaiako/issues/14))
- Fix email address in footer. ([fixes #93](https://github.com/uccser/dthm4kaiako/issues/93))
- Fix displaying events if not public. ([fixes #94](https://github.com/uccser/dthm4kaiako/issues/94))

## 0.5.2

- Update favicon to be readable. ([fixes #46](https://github.com/uccser/dthm4kaiako/issues/46))
- Add TinyMCE editor for session inline forms on admin site. ([fixes #83](https://github.com/uccser/dthm4kaiako/issues/83))

## 0.5.1

- Align series logo correctly with text on event page.
- Select and delete excess TinyMCE plugins. ([fixes #80](https://github.com/uccser/dthm4kaiako/issues/80))

## 0.5.0

- Display event title correctly for series event. ([fixes #77](https://github.com/uccser/dthm4kaiako/issues/77))
- Display location of event on complete NZ map. ([fixes #76](https://github.com/uccser/dthm4kaiako/issues/76))
- Add flat pages. ([fixes #75](https://github.com/uccser/dthm4kaiako/issues/75))
- Allow HTML in event session titles and descriptions, using TinyMCE. ([fixes #73](https://github.com/uccser/dthm4kaiako/issues/73))
- Add UC logo to homepage frontend. ([fixes #64](https://github.com/uccser/dthm4kaiako/issues/64))
- Align series image with text correctly.

## 0.4.3

- Fix bug where ThirdPartyEvents cannot be created as they do not contain a series attribute. ([fixes #62](https://github.com/uccser/dthm4kaiako/issues/62))
- Alter design of series cards to contain subtitle formatting. ([fixes #61](https://github.com/uccser/dthm4kaiako/issues/61))
- Increase size of sponsor logos to be clearer.

## 0.4.2

- Fix bug where series logo was prefixed with local media location. ([fixes #58](https://github.com/uccser/dthm4kaiako/issues/58))
- Add and display series subtitle.
- Format event resource count on schedule to stand out from description.

## 0.4.1

- Fix bug where admin interface does not allow changing object containing image. ([fixes #56](https://github.com/uccser/dthm4kaiako/issues/56))
- Fix name of EventImage to Event relationship. ([fixes #55](https://github.com/uccser/dthm4kaiako/issues/55))
- Fix bug where sponsor logo was prefixed with local media location.

## 0.4.0

- Allow event to be part of series. ([fixes #44](https://github.com/uccser/dthm4kaiako/issues/44))
- Do not require sponsor for an event. ([fixes #41](https://github.com/uccser/dthm4kaiako/issues/41))
- Allow media uploads for objects. ([fixes #45](https://github.com/uccser/dthm4kaiako/issues/45))
- Add start and end date fields directly to event model. ([fixes #52](https://github.com/uccser/dthm4kaiako/issues/52))
- Add warning to third party event page. ([fixes #42](https://github.com/uccser/dthm4kaiako/issues/42))
- Show third party event description as full width. ([fixes #40](https://github.com/uccser/dthm4kaiako/issues/40))
- Display resource count for each session on event page. ([fixes #51](https://github.com/uccser/dthm4kaiako/issues/51))
- Open resources and sponsors in new tab. ([fixes #48](https://github.com/uccser/dthm4kaiako/issues/48))
- Remove restriction of unique event names. ([fixes #43](https://github.com/uccser/dthm4kaiako/issues/43))
- Add test suite and code coverage. ([fixes #29](https://github.com/uccser/dthm4kaiako/issues/29))

## 0.3.1

- Fix third party event page bug. ([fixes #37](https://github.com/uccser/dthm4kaiako/issues/37))
- Fix navbar layout on mobile devices. ([fixes #38](https://github.com/uccser/dthm4kaiako/issues/38))
- Display third party URL link as button for consistency.

## 0.3.0

- Fix typo on homepage.
- Add favicon. ([fixes #11](https://github.com/uccser/dthm4kaiako/issues/11))
- Display locations with Google Maps. ([fixes #20](https://github.com/uccser/dthm4kaiako/issues/20))
- Add version number context processor and display version on website.

## 0.2.0

- Update django from 1.11.2 to 1.11.3.
- Fix bug where event has no primary location. ([fixes #26](https://github.com/uccser/dthm4kaiako/issues/26))
- Fix bug in third party admin interface. ([fixes #27](https://github.com/uccser/dthm4kaiako/issues/27))
- Add migration file for event slug changes.
- Add location to event list page.
- Fix template when multiple events are displayed.
- Add continous testing by Travis CI (includes style checks). ([fixes #28](https://github.com/uccser/dthm4kaiako/issues/28))
- Add PyUP support.

## 0.1.0

Initial release of website on Heroku.

Allows storing and viewing of:

- Official events
- Third party events
- Sessions
- Locations
- Resources
- Sponsors
