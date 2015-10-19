# -*- coding: utf-8 -*-
import glob
import os
import polib
from django import VERSION as DJANGO_VERSION
from django.core.management.commands.makemessages import (
    Command as OriginalMakeMessagesCommand)
from django.utils import translation
from django.utils.translation.trans_real import CONTEXT_SEPARATOR


class Command(OriginalMakeMessagesCommand):
    # Django version 1.7+ requires_model_validation is deprecated
    # and the value of 'requires_system_checks' is used (which is defined in
    # the original command). The attribute is completely removed in Django 1.9.
    if DJANGO_VERSION < (1, 7):
        requires_model_validation = False
    can_import_settings = True

    def handle_noargs(self, *args, **options):
        from django.conf import settings
        super(Command, self).handle_noargs(*args, **options)
        locale = options.get('locale')
        domain = options.get('domain')
        verbosity = int(options.get('verbosity'))
        process_all = options.get('all')

        # now that we've built the regular po files, we mark any translations that are already translated elsewhere
        # as obsolete. If there is already a translation in the local po file, we keep it.
        localedir = os.path.abspath('locale')
        locales = []
        if locale is not None:
            locales.append(locale)
        elif process_all:
            locale_dirs = filter(os.path.isdir, glob.glob('%s/*' % localedir))
            locales = [os.path.basename(l) for l in locale_dirs]

        # monkeypatch settings to not include the project locale directory
        localepaths = [os.path.normpath(path) for path in settings.LOCALE_PATHS]
        # remove the locale we're currently writing to from the settings, so that we can check for existing translations
        # NOT in this file
        localepaths = [path for path in localepaths if not path == localedir]
        settings.LOCALE_PATHS = list(localepaths)

        missing = object()
        for locale in locales:
            translation.activate(locale)
            catalog = translation.trans_real.catalog()
            # catalog = trans.translation(locale)
            # catalog = translation.trans_real.translation._fetch(locale)
            # catalog._fallback = False
            if verbosity > 0:
                self.stdout.write("cleaning translations for language %s " % locale)
                if locale in ['en', 'en-us']:
                    self.stdout.write(" (unreliable because %s is usually not translated) " % locale)

            basedir = os.path.join(localedir, locale, 'LC_MESSAGES')
            pofile = os.path.join(basedir, '%s.po' % domain)
            mofile = os.path.join(basedir, '%s.mo' % domain)
            po = polib.pofile(pofile)
            obsolete_count = 0
            for entry in po:
                # if entry.msgid_plural and locale == 'de': import ipdb; ipdb.set_trace()
                # if entry.msgid == 'one translation' and locale == 'de': import ipdb; ipdb.set_trace()
                context = entry.msgctxt or None
                if entry.msgid_plural:
                    if context:
                        msg = catalog._catalog.get((u"%s%s%s" % (context, CONTEXT_SEPARATOR, entry.msgid), True), missing)
                    else:
                        msg = catalog._catalog.get((entry.msgid, True), missing)
                else:
                    if context:
                        msg = catalog._catalog.get(u"%s%s%s" % (context, CONTEXT_SEPARATOR, entry.msgid), missing)
                    else:
                        msg = catalog._catalog.get(entry.msgid, missing)

                is_already_translated_elsewhere = not msg is missing
                if not entry.msgstr and is_already_translated_elsewhere:
                    entry.obsolete = 1
                    obsolete_count += 1
                    if verbosity > 0:
                        self.stdout.write(".")
            po.save(pofile)
            # po.save_as_mofile(mofile)  # should be done by regular compilemessages
            self.stdout.write(u" marked %s obsolete translations\n" % obsolete_count)
