# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Intro.for_email'
        db.alter_column(u'intro_intro', 'for_email', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Changing field 'Intro.to_email'
        db.alter_column(u'intro_intro', 'to_email', self.gf('django.db.models.fields.EmailField')(max_length=75))

        # Changing field 'Intro.for_name'
        db.alter_column(u'intro_intro', 'for_name', self.gf('django.db.models.fields.CharField')(max_length=75))

        # Changing field 'Intro.to_name'
        db.alter_column(u'intro_intro', 'to_name', self.gf('django.db.models.fields.CharField')(max_length=75))

    def backwards(self, orm):

        # Changing field 'Intro.for_email'
        db.alter_column(u'intro_intro', 'for_email', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Intro.to_email'
        db.alter_column(u'intro_intro', 'to_email', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Intro.for_name'
        db.alter_column(u'intro_intro', 'for_name', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Changing field 'Intro.to_name'
        db.alter_column(u'intro_intro', 'to_name', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'intro.intro': {
            'Meta': {'object_name': 'Intro'},
            'connected': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'for_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'for_name': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'to_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'to_name': ('django.db.models.fields.CharField', [], {'max_length': '75'})
        }
    }

    complete_apps = ['intro']