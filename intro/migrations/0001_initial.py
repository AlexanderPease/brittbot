# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Intro'
        db.create_table(u'intro_intro', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('to_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('to_email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('for_name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('for_email', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('purpose', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('sent', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('connected', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'intro', ['Intro'])


    def backwards(self, orm):
        # Deleting model 'Intro'
        db.delete_table(u'intro_intro')


    models = {
        u'intro.intro': {
            'Meta': {'object_name': 'Intro'},
            'connected': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'for_email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'for_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'purpose': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'sent': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'to_email': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'to_name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['intro']