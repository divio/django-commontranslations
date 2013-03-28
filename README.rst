django-commontranslations
=========================


django-commontranslations solves the problem that you have repeating translations across apps and projects. It is
opinionated about how project specific templates are loaded. The standard ``makemessages`` command will create a
``.po`` file with all translation strings that it finds the project directory, regardless if it makes sense to
explicitly translate them in the context of your project again.
It might just be an app template that was overridden in the project, with all the translated strings already translated
in the app.

django-commontranslations contains:

* a modified ``makemessages`` command that will mark untranslated entries as obsolete if they have already been
  translated elsewhere.
* a set of well structured translations of commonly used terms to use in other apps (just add django-commontranslations
  as a dependency and add ``django_commontranslations`` to ``INSTALLED_APPS``) [IRONICALLY NOT TRANSLATED YET]
* intructions on how to use common translations in your own apps (not yet)


django-commontranslations assumes that your project specific translations reside in a directory configured
in the ``LOCALE_PATHS`` setting. It is assumed that ``LANGUAGE_CODE`` (the default language) is always ``en`` or
``en-us``.