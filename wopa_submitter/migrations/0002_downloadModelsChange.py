# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'wopa_submitter_document')

        # Adding model 'ReadingDocuments'
        db.create_table(u'wopa_submitter_readingdocuments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['ReadingDocuments'])

        # Adding model 'SubmissionDocuments'
        db.create_table(u'wopa_submitter_submissiondocuments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['SubmissionDocuments'])

        # Adding model 'AssignmentDocuments'
        db.create_table(u'wopa_submitter_assignmentdocuments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['AssignmentDocuments'])


        # Renaming column for 'Reading.file' to match new field type.
        db.rename_column(u'wopa_submitter_reading', 'file', 'file_id')
        # Changing field 'Reading.file'
        db.alter_column(u'wopa_submitter_reading', 'file_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wopa_submitter.ReadingDocuments']))
        # Adding index on 'Reading', fields ['file']
        db.create_index(u'wopa_submitter_reading', ['file_id'])


        # Renaming column for 'Assignment.assignment_file' to match new field type.
        db.rename_column(u'wopa_submitter_assignment', 'assignment_file', 'assignment_file_id')
        # Changing field 'Assignment.assignment_file'
        db.alter_column(u'wopa_submitter_assignment', 'assignment_file_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wopa_submitter.AssignmentDocuments']))
        # Adding index on 'Assignment', fields ['assignment_file']
        db.create_index(u'wopa_submitter_assignment', ['assignment_file_id'])


    def backwards(self, orm):
        # Removing index on 'Assignment', fields ['assignment_file']
        db.delete_index(u'wopa_submitter_assignment', ['assignment_file_id'])

        # Removing index on 'Reading', fields ['file']
        db.delete_index(u'wopa_submitter_reading', ['file_id'])

        # Adding model 'Document'
        db.create_table(u'wopa_submitter_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('docfile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'wopa_submitter', ['Document'])

        # Deleting model 'ReadingDocuments'
        db.delete_table(u'wopa_submitter_readingdocuments')

        # Deleting model 'SubmissionDocuments'
        db.delete_table(u'wopa_submitter_submissiondocuments')

        # Deleting model 'AssignmentDocuments'
        db.delete_table(u'wopa_submitter_assignmentdocuments')


        # Renaming column for 'Reading.file' to match new field type.
        db.rename_column(u'wopa_submitter_reading', 'file_id', 'file')
        # Changing field 'Reading.file'
        db.alter_column(u'wopa_submitter_reading', 'file', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Renaming column for 'Assignment.assignment_file' to match new field type.
        db.rename_column(u'wopa_submitter_assignment', 'assignment_file_id', 'assignment_file')
        # Changing field 'Assignment.assignment_file'
        db.alter_column(u'wopa_submitter_assignment', 'assignment_file', self.gf('django.db.models.fields.files.FileField')(max_length=100))

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
            'assignment_file': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.AssignmentDocuments']"}),
            'details': ('django.db.models.fields.TextField', [], {}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_published': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'wopa_submitter.assignmentdocuments': {
            'Meta': {'object_name': 'AssignmentDocuments'},
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
            'file': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.ReadingDocuments']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        u'wopa_submitter.readingdocuments': {
            'Meta': {'object_name': 'ReadingDocuments'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'wopa_submitter.submission': {
            'Meta': {'object_name': 'Submission'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.Assignment']"}),
            'date_submitted': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'documents': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['wopa_submitter.SubmissionDocuments']", 'null': 'True', 'symmetrical': 'False'}),
            'feedback': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['wopa_submitter.Feedback']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'wopa_submitter.submissiondocuments': {
            'Meta': {'object_name': 'SubmissionDocuments'},
            'docfile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['wopa_submitter']