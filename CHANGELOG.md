# Changelog

## 0.18.3

- Update 'Get Started' label from 'Coming April 2020' to 'Coming Late 2020'.

## 0.18.2

- Store authors for resources (users and/or entities).
    - Searching and filtering by authors will be added at a later time.
- Improve layout of information for resources on their detail pages.
- Alter resource and event card colours to match their hub's theme.
- Fix CSS bug where hyperlinks appeared on whitespace between logos on homepage.
- Add validation within admin interface to check at least one author for a resource.
- Add spacing between resource components in admin.

## 0.18.1

- Set path for loading SVGs.
- Use padded logos to ensure even vertical sizing of logos.

## 0.18.0

- Add entity model for managing all organisations, companies, groups, etc and migrate data to this model.
- Update brand icons and colours.
- Add placeholder for upcoming 'Get Started' guide.
- Add 'invite only' event registration type.
- Darken events hub colour to meet AA contrast text rating.
- Set CORS settings for static file servers.

## 0.17.6

- Improve readabilty of event title and sponsors with increased whitespace.
- Fix bug where event series image was not centered in sidebar.
- Fix bug where event header images were not consistent sizes.

## 0.17.5

- Hide registration link if no link is provided. (fixes #544)
- Allow setting of type of event registration (normal/application based/external website). (fixes #543)
- Show published status on event admin list. (fixes #540)
- Add ability to duplicate events in admin interface.
- Enable event badge and organiser links.
- Update location picker for event sessions to use same widget as event locations. (fixes #542)
- Fix bug where maps JavaScript was run when no map was available.
- Update event card and detail pages to show series in a clearer way. (fixes #541)
- Update AATEA logo. (fixes #546)
- Show number of returned events from filters.
- Set event sessions to be ordered by name, after start and end times.
- Update sample data script to provide wider range of event data.

## 0.17.4

- Redesign event hub to list events in two categories, upcoming events or past events. Both categories have filtering enabled on key attributes.
- Allow event schedule to be hidden for simple events.
- Fix bug where maps were not showing locations.
- Fix bug were extra character showed in event descriptions.
- Remove duplicate information on event pages.
- Add buttons for event administrators to easily edit events from website.
- Improve listing of locations in event admin.
- Improve search for event locations in event admin.

## 0.17.3

- Improve display of location addresses, by adding 'region' to the end of region names to avoid confusion with city names.
- Show sponsor on event sidebar.
- Fix bug where repeated sessions on consecutive event days did not display session times.
- Update Travis CI configuration file to latest standard.
- Dependencies changes:
    - Update argon2-cffi from 19.1.0 to 19.2.0.
    - Update coverage from 4.5.4 to 5.0.3.
    - Update django-activeurl from 0.1.12 to 0.2.0.
    - Update django-allauth from 0.40.0 to 0.41.0.
    - Update django-autoslug-iplweb from 1.9.4 to 1.9.5.
    - Update django-ckeditor from 5.7.1 to 5.9.0.
    - Update django-coverage-plugin from 1.6.0 to 1.8.0.
    - Update django-crispy-forms from 1.7.2. to 1.8.1.
    - Update django-debug-toolbar from 2.0 to 2.2.
    - Update django-extensions from 2.2.1 to 2.2.6.
    - Update django-model-utils from 3.2.0 to 4.0.0.
    - Update django-recaptcha from 2.0.5 to 2.0.6.
    - Update django-redis from 4.10.0 to 4.11.0.
    - Update django-storages from 1.7.2 from 1.9.1.
    - Update djangorestframework from 3.10.2 to 3.11.0.
    - Update flake8 from 3.7.8 to 3.7.9.
    - Update google-auth from 1.6.3 to 1.11.0.
    - Update google-cloud-logging from 1.12.1 to 1.14.0.
    - Update google-cloud-storage from 1.19.1 to 1.25.0.
    - Update google-resumable-media from 0.4.1 to 0.5.0.
    - Update mypy from 0.720 to 0.761.
    - Update Pillow from 6.1.0 to 7.0.0.
    - Update psycopg2-binary from 2.8.3 to 2.8.4.
    - Update pydocstyle from 4.0.1 to 5.0.2.
    - Update pytest from 5.1.0 to 5.3.5.
    - Update pytest-django from 3.5.1 to 3.8.0.
    - Update python-slugify from 3.0.4 to 4.0.0.
    - Update pytz from 2019.2 to 2019.3.
    - Update Sphinx from 2.1.2 to 2.3.1.

## 0.17.2

- Update number of DTTA members.
- Add list of DTTA committee members.
- Use default Google App Engine settings for split health checks.

## 0.17.1

- Minor changes to TENZ puzzle page.

## 0.17.0

- Add secret pages application.
- Update LICENSE to include license exclusions.
- Dependencies changes:
    - Update python-slugify from 3.0.3 to 3.0.4.
    - Update django-anymail from 6.1.0 to 7.0.0.
    - Update django-allauth from 0.39.1 to 0.40.0.
    - Update django-recaptcha from 2.0.4 to 2.0.5.
    - Update django-storages from 1.7.1 to 1.7.2.
    - Update google-cloud-storage from 1.18.0 to 1.19.1.
    - Update google-resumable-media from 0.3.2 to 0.4.1.

## 0.16.6

- Fix bug where empty progress outcome data was shown in POET admin.

## 0.16.5

- Show top three crowdsourced progress outcomes with submission threshold in POET admin.
- Prevent images from overflowing from parent in resource descriptions.
- Remove empty footer link.
- Fix bug where email in contact form response was omitted.

## 0.16.4

- Improve statistics page for POET admin.
- Dependencies changes:
    - Update google-api-python-client from 1.7.10 to 1.7.11.
    - Update pydocstyle from 4.0.0 to 4.0.1.
    - Update pytest from 4.6.3 to 5.1.0.

## 0.16.3

- Raise level of logging messages to Google Stackdriver to prevent excess logging.
- Set lifetime of database connections to zero.
- Tidy logic for sending 'Contact Us' emails.

## 0.16.2

- Progress Outcome Evaluation Tool (POET) updates:
    - Feedback is now listed on admin statistics page.
    - Fix bug where resource statistics page couldn't be loaded if no submissions existed for it.
    - Add indicator for active progress outcome groups in admin interface.
- Connected Django improved logging to GCP Stackdriver.
- Fix bug where know reCAPTCHA keys were used.
- Dependencies changes:
    - Add google-cloud-logging 1.12.1.

## 0.16.1

- Progress Outcome Evaluation Tool (POET) updates:
    - Add about page.
    - Add contact us page.
    - Improve feedback messages to user.
    - Add tooltips for progress outcome choices.
    - Increase threshold for showing statistics.
    - Add statistic pages for staff.
    - Remove resume feature as it was confusing to users.
- Dependencies changes:
    - Update coverage from 4.5.3 to 4.5.4.
    - Update django-anymail from 6.0.1 to 6.1.0.
    - Update django-debug-toolbar from 1.11 to 2.0.
    - Update django-extensions from 2.1.9 to 2.2.1.
    - Update django-filter from 2.1.0 to 2.2.0.
    - Update djangorestframework from 3.9.4 to 3.10.2.
    - Update flake8 from 3.7.7 to 3.7.8.
    - Update google-api-python-client from 1.7.9 to 1.7.10.
    - Update mypy from 0.711 to 0.720.
    - Update pillow from 6.0.0 to 6.1.0.
    - Update pydocstyle from 3.0.0 to 4.0.0.
    - Update pytest-django from 3.5.0 to 3.5.1.
    - Update python-slugify from 3.0.2 to 3.0.3.
    - Update pytz from 2019.1 to 2019.2.
- Require reCAPTCHA for all contact forms on website.
- Remove cron job tasks.

## 0.16.0

- Add Progress Outcome Evaluation Tool (POET) application.

## 0.15.2

- Change default ordering of event locations to be alphabetical.

## 0.15.1

- Fix out of index error for learning area cards webpage.

## 0.15.0

- Change name of 'Authentic Context Cards' to 'Learning Area Cards'.
- Add progress outcome card set to learning area cards.
- Fix incorrect data for achievement objectives for learning area cards.
- Dependencies changes:
    - Update anymail[mailgun] from 6.0 to 6.0.1.
    - Update ckeditor from 5.7.0 to 5.7.1.
    - Update django-extensions from 2.1.6 to 2.1.9.
    - Update django-model-utils from 3.1.2 to 3.2.0.
    - Update google-api-python-client from 1.7.8 to 1.7.9.
    - Update google-cloud-storage from 1.15.0 to 1.16.1.
    - Update mypy from 0.670 to 0.711.
    - Update psycopg2-binary from 2.8.2 to 2.8.3.
    - Update pytest from 4.5.0 to 4.6.3.
    - Update pytest-django from 3.4.8 to 3.5.0.
    - Update Sphinx from 2.0.1 to 2.1.2.

## 0.14.2

- Add new dependency for missing library for Google Cloud Storage dependency.

## 0.14.1

- Update dependency for backup bindings for Google Cloud Storage.

## 0.14.0

- Add double sided version of authentic context cards.
- Add projects area to DTTA hub.
- Dependencies changes:
    - Update autoprefixer from 9.4.6 to 9.5.1.
    - Update babel/core from 7.2.2 to 7.4.4.
    - Update babel/preset-env from 7.3.1 to 7.4.4.
    - Update del from 3.0.0 to 4.1.1.
    - Update details-element-polyfill from 2.3.0 to 2.3.1.
    - Update django-ckeditor from 5.6.1 to 5.7.0.
    - Update djangorestframework from 3.9.2 to 3.9.4.
    - Update fuse.js from 3.4.2 to 3.4.4.
    - Update gulp from 3.9.1 to 4.0.2.
    - Update gulp-sourcemaps from 2.6.4 to 2.6.5.
    - Update jshint from 2.9.7 to 2.10.2.
    - Update jquery from 3.3.1 to 3.4.1.
    - Update node-gyp from 3.8.0 to 4.0.0.
    - Update Pillow from 5.4.1 to 6.0.0.
    - Update popper.js from 1.14.7 to 1.15.0.
    - Update python-slugify from 3.0.0 to 3.0.2.
    - Update pytz from 2018.9 to 2019.1.
    - Update yargs from 12.0.5 to 13.2.4.
    - Update Sphinx from 1.8.5 to 2.0.1.
    - Update psycopg2-binary from 2.7.7 to 2.8.2.
    - Update pytest from 4.3.1 to 4.5.0.
    - Update factory-boy from 2.11.1 to 2.12.0.

## 0.13.3

- Add published attribute to resources.

## 0.13.2

- Fix bug where event organisers are not shown on an event card.

## 0.13.1

- Fix bug where authentic context cards are empty.
- Fix deployment of cron job for production deployment.
- Show log of updating achievement objectives.

## 0.13.0

- Redesign homepage to highlight key entrypoints to the website. ([fixes #314](https://github.com/uccser/dthm4kaiako/issues/314))
- Add authentic context cards website. ([fixes #294](https://github.com/uccser/dthm4kaiako/issues/294))
- Allow events to be featured on the website. ([fixes #317](https://github.com/uccser/dthm4kaiako/issues/317))
- Improve design of event cards to clearly show organisers and series.
- Allow nodes on event map to show future events at each location. ([fixes #313](https://github.com/uccser/dthm4kaiako/issues/313))
- Add map clustering to events map.
- Order event organisers and sponsors in alphabetical order by name.
- Order event locations by region, then city, then name (roughly listed north to south across New Zealand).
- Improve listing of events on admin site.
- Increase contrast between NZQA standard levels. ([fixes #320](https://github.com/uccser/dthm4kaiako/issues/320))
- Fix bug where technological areas not showing on a resource detail. ([fixes #321](https://github.com/uccser/dthm4kaiako/issues/321))
- Fix bug where event times wouldn't fit correctly. ([fixes #325](https://github.com/uccser/dthm4kaiako/issues/325))
- Dependencies changes:
    - Update Sphinx from 1.8.4 to 1.8.5.
    - Update pytest from 4.3.0 to 4.3.1.
    - Update coverage from 4.5.2 to 4.5.3.
    - Remove Werkzeug dependency.
    - Remove ipdb dependency.

## 0.12.1

- Do not require a description for an event session.
- Display missing fields for events in admin interface.
- Allow event start and end datetimes to be empty until sessions are created.
- Fix bug where 500 error page couldn't load.

## 0.12.0

- Add basic events hub. ([fixes #296](https://github.com/uccser/dthm4kaiako/issues/296))
    - Replaces the existing cs4teachers.org.nz website.
    - Use geographical information system (GIS) to store and process location data.
    - Events can either be onsite, online, or both.
    - Events can have multiple sponsors, organisers, and sessions.
    - Events and sessions can have multiple locations.
    - Add sample data generator for event hub for testing.
- Increase number of news articles on DTTA homepage to show last month of articles. ([fixes #301](https://github.com/uccser/dthm4kaiako/issues/301))
- Store type and credits for NZQA achievement standards. ([fixes #304](https://github.com/uccser/dthm4kaiako/issues/304))
- Increase number of workers on website servers. ([fixes #298](https://github.com/uccser/dthm4kaiako/issues/298))
- Dependencies changes:
    - Update python-slugify from 2.0.1 to 3.0.0.
    - Update django-allauth from 0.39.0 to 0.39.1.
    - Update djangorestframework from 3.9.1 to 3.9.2.
    - Add django-map-widgets 0.2.2.

## 0.11.0

- Add resource search and filtering.
- Resource badges are now a shortcut to the search page filtered by that badge.
- Create development server for testing. ([fixes #209](https://github.com/uccser/dthm4kaiako/issues/209))
- Dependencies changes:
    - Update bootstrap from 4.2.1 to 4.3.1.
    - Update fuse.js from 3.3.0 to 3.4.2.
    - Update popper.js from 1.14.6 to 1.14.7.
    - Update django-anymail from 5.0 to 6.0.
    - Update django-allauth from 0.38.0 to 0.39.0.
    - Add django-haystack with Elasticsearch 5 support.
    - Add elasticsearch 5.5.3.
    - Update flake8 from 3.7.6 to 3.7.7.
    - Update django-extensions from 2.1.5 to 2.1.6.
    - Update pytest-django from 3.4.7 to 3.4.8.
    - Update google-auth from 1.6.2 to 1.6.3.

## 0.10.1

- Update production secrets.

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
