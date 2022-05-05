User media uploads are stored on Google Cloud Platform in a storage bucket.
Storing user uploads requires high reliably, and also management of access to specific items.
Self hosted exiting solutions with matching features were either overly complex or resource intensive to run.
Self hosting a network drive across all swarm nodes would likely work if all files were publicly accessible.
The decision to use Google Cloud Platform was due to it's simplicity, cheap costs (~$5 a month), and files were already hosted there.
