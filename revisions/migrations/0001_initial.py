# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventDataDump'
        db.create_table('revisions_eventdatadump', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('event_data', self.gf('jsonfield.fields.JSONField')()),
        ))
        db.send_create_signal('revisions', ['EventDataDump'])

        # Adding model 'Event'
        db.create_table('revisions_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event_code', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('event_subcode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('revisions', ['Event'])

        # Adding model 'Revision'
        db.create_table('revisions_revision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['revisions.Event'])),
            ('event_note', self.gf('django.db.models.fields.TextField')()),
            ('note_hash', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('diff_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1, max_length=3)),
            ('count', self.gf('django.db.models.fields.IntegerField')(max_length=5)),
            ('update', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['revisions.EventDataDump'])),
            ('update_by', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('revisions', ['Revision'])


    def backwards(self, orm):
        # Deleting model 'EventDataDump'
        db.delete_table('revisions_eventdatadump')

        # Deleting model 'Event'
        db.delete_table('revisions_event')

        # Deleting model 'Revision'
        db.delete_table('revisions_revision')


    models = {
        'revisions.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event_code': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'event_subcode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'revisions.eventdatadump': {
            'Meta': {'object_name': 'EventDataDump'},
            'event_data': ('jsonfield.fields.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'revisions.revision': {
            'Meta': {'object_name': 'Revision'},
            'count': ('django.db.models.fields.IntegerField', [], {'max_length': '5'}),
            'diff_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['revisions.Event']"}),
            'event_note': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'note_hash': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1', 'max_length': '3'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'update': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['revisions.EventDataDump']"}),
            'update_by': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['revisions']