# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Assignment'
        db.create_table(u'wopa_submitter_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('about', self.gf('django.db.models.fields.TextField')()),
            ('details', self.gf('django.db.models.fields.TextField')()),
            ('is_published', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['Assignment'])

        # Adding model 'Feedback'
        db.create_table(u'wopa_submitter_feedback', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thefeedback', self.gf('django.db.models.fields.TextField')()),
            ('marker', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'wopa_submitter', ['Feedback'])

        # Adding model 'SubmissionDocument'
        db.create_table(u'wopa_submitter_submissiondocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('submitter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['SubmissionDocument'])

        # Adding model 'Submission'
        db.create_table(u'wopa_submitter_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('assignment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wopa_submitter.Assignment'])),
            ('feeling_about_assignment', self.gf('django.db.models.fields.TextField')()),
            ('feedback', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wopa_submitter.Feedback'], null=True)),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_submitted', self.gf('django.db.models.fields.DateField')(null=True)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['Submission'])

        # Adding model 'Reading'
        db.create_table(u'wopa_submitter_reading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('document', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['Reading'])

        # Adding model 'ReadingDocument'
        db.create_table(u'wopa_submitter_readingdocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['ReadingDocument'])

        # Adding model 'AssignmentDocument'
        db.create_table(u'wopa_submitter_assignmentdocument', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assignment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wopa_submitter.Assignment'], unique=True, null=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['AssignmentDocument'])


    def backwards(self, orm):
        # Deleting model 'Assignment'
        db.delete_table(u'wopa_submitter_assignment')

        # Deleting model 'Feedback'
        db.delete_table(u'wopa_submitter_feedback')

        # Deleting model 'SubmissionDocument'
        db.delete_table(u'wopa_submitter_submissiondocument')

        # Deleting model 'Submission'
        db.delete_table(u'wopa_submitter_submission')

        # Deleting model 'Reading'
        db.delete_table(u'wopa_submitter_reading')

        # Deleting model 'ReadingDocument'
        db.delete_table(u'wopa_submitter_readingdocument')

        # Deleting model 'AssignmentDocument'
        db.delete_table(u'wopa_submitter_assignmentdocument')


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
            'details': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'wopa_submitter.assignmentdocument': {
            'Meta': {'object_name': 'AssignmentDocument'},
            'assignment': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wopa_submitter.Assignment']", 'unique': 'True', 'null': 'True'}),
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
            'document': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'wopa_submitter.readingdocument': {
            'Meta': {'object_name': 'ReadingDocument'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'wopa_submitter.submission': {
            'Meta': {'object_name': 'Submission'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.Assignment']"}),
            'date_submitted': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.Feedback']", 'null': 'True'}),
            'feeling_about_assignment': ('django.db.models.fields.TextField', [], {}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'wopa_submitter.submissiondocument': {
            'Meta': {'object_name': 'SubmissionDocument'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submitter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['wopa_submitter']