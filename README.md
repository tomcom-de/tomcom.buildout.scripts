Information
===========

This package install some helper scripts to make buildout handling in some parts more handy. You can find the helper scripts in your INSTANCE/bin directory.


**upgrade_version**

If you want to upgrade your project to a newer version you can use this script.
Your need a version.cfg for your current project and a version.cfg of the next release.

The version numbers in the next release will be replaced in the version.cfg of your current
project.

TO KNOW:

- The sections has to be the same.
- Completely new versions in a section will be added.
- Newer Version in the old versions.cfg will not be overridden.
- Versions who shoud be upgraded but are not in the new version.cfg
  will not be handled. So it's every time possible that you have to modify
  some versions by your own. Depending on the 3rd party packages you installed.

**pin_version**

Builds a new versions.cfg file. All Versions wich are used in egg form are included.
