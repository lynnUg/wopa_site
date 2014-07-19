# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'wopa_submitter_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['Document'])

        # Adding model 'Assignment'
        db.create_table(u'wopa_submitter_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('about', self.gf('django.db.models.fields.TextField')()),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assignment_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'wopa_submitter', ['Assignment'])

        # Adding model 'Feedback'
        db.create_table(u'wopa_submitter_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thefeedback', self.gf('django.db.models.fields.TextField')()),
            ('marker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'wopa_submitter', ['Feedback'])

        # Adding model 'Submission'
        db.create_table(u'wopa_submitter_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wopa_submitter.Assignment'])),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wopa_submitter.Feedback'], null=True)),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_submitted', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'wopa_submitter', ['Submission'])

        # Adding M2M table for field documents on 'Submission'
        m2m_table_name = db.shorten_name(u'wopa_submitter_submission_documents')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('submission', models.ForeignKey(orm[u'wopa_submitter.submission'], null=False)),
            ('document', models.ForeignKey(orm[u'wopa_submitter.document'], null=False))
        ))
        db.create_unique(m2m_table_name, ['submission_id', 'document_id'])

        # Adding model 'Reading'
        db.create_table(u'wopa_submitter_reading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'wopa_submitter', ['Reading'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'wopa_submitter_document')

        # Deleting model 'Assignment'
        db.delete_table(u'wopa_submitter_assignment')

        # Deleting model 'Feedback'
        db.delete_table(u'wopa_submitter_feedback')

        # Deleting model 'Submission'
        db.delete_table(u'wopa_submitter_submission')

        # Removing M2M table for field documents on 'Submission'
        db.delete_table(db.shorten_name(u'wopa_submitter_submission_documents'))

        # Deleting model 'Reading'
        db.delete_table(u'wopa_submitter_reading')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'wopa_submitter.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'about': ('django.db.models.fields.TextField', [], {}),
            'assignment_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'wopa_submitter.document': {
            'Meta': {'object_name': 'Document'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'wopa_submitter.feedback': {
            'Meta': {'object_name': 'Feedback'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marker': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'thefeedback': ('django.db.models.fields.TextField', [], {})
        },
        u'wopa_submitter.reading': {
            'Meta': {'object_name': 'Reading'},
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'wopa_submitter.submission': {
            'Meta': {'object_name': 'Submission'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.Assignment']"}),
            'date_submitted': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['wopa_submitter.Document']", 'null': 'True', 'symmetrical': 'False'}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.Feedback']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['wopa_submitter']