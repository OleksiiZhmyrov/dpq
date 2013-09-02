# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Statistics'
        db.create_table('queue_statistics', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('number_of_pushes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('total_push_duration', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('queue', ['Statistics'])

        # Adding model 'Branch'
        db.create_table('queue_branch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('finish_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('queue', ['Branch'])

        # Adding model 'Team'
        db.create_table('queue_team', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('css_icon', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('queue', ['Team'])

        # Adding model 'UserStory'
        db.create_table('queue_userstory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('assignee', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('tester', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('last_sync', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('queue', ['UserStory'])

        # Adding model 'QueueRecord'
        db.create_table('queue_queuerecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.UserStory'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('queue_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')(unique=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Branch'])),
            ('team', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Team'], null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('push_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('done_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='W', max_length=1)),
        ))
        db.send_create_signal('queue', ['QueueRecord'])

        # Adding model 'Role'
        db.create_table('queue_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('can_create_records', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('can_modify_own_records', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('can_modify_all_records', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('queue', ['Role'])

        # Adding model 'CustomUserRecord'
        db.create_table('queue_customuserrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('django_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('role', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['queue.Role'])),
        ))
        db.send_create_signal('queue', ['CustomUserRecord'])


    def backwards(self, orm):
        # Deleting model 'Statistics'
        db.delete_table('queue_statistics')

        # Deleting model 'Branch'
        db.delete_table('queue_branch')

        # Deleting model 'Team'
        db.delete_table('queue_team')

        # Deleting model 'UserStory'
        db.delete_table('queue_userstory')

        # Deleting model 'QueueRecord'
        db.delete_table('queue_queuerecord')

        # Deleting model 'Role'
        db.delete_table('queue_role')

        # Deleting model 'CustomUserRecord'
        db.delete_table('queue_customuserrecord')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'queue.branch': {
            'Meta': {'object_name': 'Branch'},
            'finish_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'start_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'queue.customuserrecord': {
            'Meta': {'object_name': 'CustomUserRecord'},
            'django_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Role']"})
        },
        'queue.queuerecord': {
            'Meta': {'object_name': 'QueueRecord'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Branch']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'done_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {'unique': 'True'}),
            'modified_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'push_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'queue_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'W'", 'max_length': '1'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.UserStory']"}),
            'team': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['queue.Team']", 'null': 'True', 'blank': 'True'})
        },
        'queue.role': {
            'Meta': {'object_name': 'Role'},
            'can_create_records': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'can_modify_all_records': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'can_modify_own_records': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'queue.statistics': {
            'Meta': {'object_name': 'Statistics'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number_of_pushes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_push_duration': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'queue.team': {
            'Meta': {'object_name': 'Team'},
            'css_icon': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'queue.userstory': {
            'Meta': {'object_name': 'UserStory'},
            'assignee': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tester': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['queue']