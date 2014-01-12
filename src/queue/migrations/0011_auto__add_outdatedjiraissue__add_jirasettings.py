# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OutdatedJiraIssue'
        db.create_table(u'queue_outdatedjiraissue', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
            ('assignee', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('tester', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('reporter', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('epic', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('team', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('is_deskcheck', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'queue', ['OutdatedJiraIssue'])

        # Adding model 'JiraSettings'
        db.create_table(u'queue_jirasettings', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('browse_url', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('project_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
        ))
        db.send_create_signal(u'queue', ['JiraSettings'])


    def backwards(self, orm):
        # Deleting model 'OutdatedJiraIssue'
        db.delete_table(u'queue_outdatedjiraissue')

        # Deleting model 'JiraSettings'
        db.delete_table(u'queue_jirasettings')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'queue.boardsticker': {
            'Meta': {'object_name': 'BoardSticker'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.CustomUserRecord']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_modified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modification_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'retroBoard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.RetroBoard']"}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'voters': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'queue.branch': {
            'Meta': {'object_name': 'Branch'},
            'build_success': ('django.db.models.fields.BooleanField', [], {}),
            'finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {}),
            'last_build_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'start_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'queue.confluencesettings': {
            'Meta': {'object_name': 'ConfluenceSettings'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'namespace': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'page_title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'queue.customuserrecord': {
            'Meta': {'object_name': 'CustomUserRecord'},
            'django_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.Role']"}),
            'trump_cards': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'queue.deskcheckstatistic': {
            'Meta': {'object_name': 'DeskCheckStatistic'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'failed_count': ('django.db.models.fields.FloatField', [], {}),
            'failed_count_sp': ('django.db.models.fields.FloatField', [], {}),
            'failed_percent': ('django.db.models.fields.FloatField', [], {}),
            'failed_percent_sp': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'other_count': ('django.db.models.fields.FloatField', [], {}),
            'other_count_sp': ('django.db.models.fields.FloatField', [], {}),
            'other_percent': ('django.db.models.fields.FloatField', [], {}),
            'other_percent_sp': ('django.db.models.fields.FloatField', [], {}),
            'passed_count': ('django.db.models.fields.FloatField', [], {}),
            'passed_count_sp': ('django.db.models.fields.FloatField', [], {}),
            'passed_percent': ('django.db.models.fields.FloatField', [], {}),
            'passed_percent_sp': ('django.db.models.fields.FloatField', [], {}),
            'ready_count': ('django.db.models.fields.FloatField', [], {}),
            'ready_count_sp': ('django.db.models.fields.FloatField', [], {}),
            'ready_percent': ('django.db.models.fields.FloatField', [], {}),
            'ready_percent_sp': ('django.db.models.fields.FloatField', [], {}),
            'total_count': ('django.db.models.fields.FloatField', [], {}),
            'total_count_sp': ('django.db.models.fields.FloatField', [], {})
        },
        u'queue.jirasettings': {
            'Meta': {'object_name': 'JiraSettings'},
            'browse_url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'project_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        u'queue.outdatedjiraissue': {
            'Meta': {'object_name': 'OutdatedJiraIssue'},
            'assignee': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'epic': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deskcheck': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reporter': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'team': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'tester': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        u'queue.queuerecord': {
            'Meta': {'object_name': 'QueueRecord'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.Branch']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'push_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'queue_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '1'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.UserStory']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.Team']", 'null': 'True', 'blank': 'True'})
        },
        u'queue.retroboard': {
            'Meta': {'object_name': 'RetroBoard'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.CustomUserRecord']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sprint': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.Sprint']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.Team']"}),
            'vote_limit': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        u'queue.role': {
            'Meta': {'object_name': 'Role'},
            'can_create_records': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_modify_all_records': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_modify_own_records': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'queue.sprint': {
            'Meta': {'object_name': 'Sprint'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'finish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motto': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'queue.statistics': {
            'Meta': {'object_name': 'Statistics'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_pushes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_push_duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'queue.team': {
            'Meta': {'object_name': 'Team'},
            'css_icon': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'queue.userstory': {
            'Meta': {'object_name': 'UserStory'},
            'assignee': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tester': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'queue.usertoretroboardconnector': {
            'Meta': {'object_name': 'UserToRetroBoardConnector'},
            'custom_user_record': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.CustomUserRecord']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retroBoard': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['queue.RetroBoard']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['queue']